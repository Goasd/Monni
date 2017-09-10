import threading
import configparser
from queue import Queue

from gi.repository import GLib

from monni.games.teeworlds.master import TeeworldsMaster
from monni.games.teeworlds.teeworlds import TeeworldsServer
from .serverslist import ServersList
from .urbanterror.master import UrbanTerrorMaster
from .game_server import GameServer
from .urbanterror.urbanterror import UrbanServer


class Settings:
    def __init__(self):
        self.file = 'config.ini'

    def settings(self):
        config = configparser.ConfigParser()
        config.read(self.file)
        print(config)

    def set_game_location(self, game, location):
        config = configparser.ConfigParser()
        config.read(self.file)
        try:
            config.set(game, 'location', location)
        except:
            config[str(game)] = {}
            config[str(game)]['location'] = location
        with open(self.file, 'w') as configfile:
            config.write(configfile)

    def get_game_location(self, game):
        try:
            config = configparser.ConfigParser()
            config.read(self.file)
            return config[game]['location']
        except:
            return ''

    def set_server_password(self, server, password):
        server_list_file = open('servers', 'r')
        server_list = eval(server_list_file.read())

        server_list_file.close()

        for s in server_list:
            if s[0] == server.host and s[1] == server.port and s[2] == server.game:
                try:
                    s[3] = password
                except:
                    pass

        server_list_file = open('servers', 'w')
        server_list_file.write(repr(server_list))
        server_list_file.close()

    def get_server_password(self, server):
        server_list_file = open('servers', 'r')
        server_list = eval(server_list_file.read())

        server_list_file.close()
        for s in server_list:
            if s[0] == server.host and s[1] == server.port and s[2] == server.game:
                try:
                    return s[3]
                except:
                    pass
        return ''

    def set_admin_password(self, server, password):
        server_list_file = open('servers', 'r')
        server_list = eval(server_list_file.read())

        server_list_file.close()

        for s in server_list:
            if s[0] == server.host and s[1] == server.port and s[2] == server.game:
                try:
                    s[4] = password
                except:
                    pass
        print(server_list)
        server_list_file = open('servers', 'w')
        server_list_file.write(repr(server_list))
        server_list_file.close()

    def get_admin_password(self, server):
        server_list_file = open('servers', 'r')
        server_list = eval(server_list_file.read())

        server_list_file.close()
        for s in server_list:
            if s[0] == server.host and s[1] == server.port and s[2] == server.game:
                try:
                    return s[4]
                except:
                    pass
        return ''


class Servers:
    def __init__(self):
        self.call_when_server_created = lambda: None
        self.call_when_server_deleted = lambda: None
        self.call_when_server_updated = lambda: None
        self.file = 'servers'
        self.q = Queue()

    def update_server_data(self, server):
        for _ in range(3):
            self.t = ServerDownloader(self.q, self.call_when_server_updated)
            self.t.setDaemon(True)
            self.t.start()
        self.q.put(server)

    def servers_add(self, server_list):

        for _ in range(3):
            t = ServerDownloader(self.q, self.call_when_server_created)
            t.setDaemon(True)
            t.start()

        for server in server_list:
            self.q.put(server)

    def servers(self):

        default_servers = [
            ['151.80.41.55', 27960, 'Urban Terror', '', '']
        ]

        try:
            server_list_file = open(self.file, 'r')
            server_list = eval(server_list_file.read())
        except FileNotFoundError:
            server_list_file = open(self.file, 'w')
            server_list_file.write(repr(default_servers))
            server_list_file.close()
            server_list_file = open(self.file, 'r')
            server_list = eval(server_list_file.read())
        server_list_file.close()

        q = Queue()

        for _ in range(3):
            t = ServerDownloader(q, self.call_when_server_created)
            t.setDaemon(True)
            t.start()

        for server in server_list:
            gameserver = GameServer()
            gameserver.host = server[0]
            gameserver.port = server[1]
            gameserver.game = server[2]
            q.put(gameserver)

    def add_server(self, hostname, port, game):

        gameserver = GameServer()
        gameserver.game = game
        gameserver.port = port
        gameserver.host = hostname

        if game == 'Urban Terror':
            UrbanServer(gameserver)
        else:
            return ValueError

        GLib.idle_add(self.call_when_server_created, gameserver)

    def add_new_server(self, hostname, port, game):

        server_list_file = open(self.file, 'r')
        server_list = eval(server_list_file.read())
        server_list.append([hostname, port, game, '', ''])

        server_list_file = open(self.file, 'w')
        server_list_file.write(repr(server_list))
        server_list_file.close()

        self.add_server(hostname, port, game)

    def delete_server(self, server):
        server_list_file = open(self.file, 'r')
        server_list = eval(server_list_file.read())

        server_list.remove([server.host, server.port, server.game, server.server_password, server.admin_password])

        server_list_file = open(self.file, 'w')
        server_list_file.write(repr(server_list))
        server_list_file.close()

        GLib.idle_add(self.call_when_server_deleted, server)

    def is_favorite_server(self, check_server):
        server_list_file = open(self.file, 'r')
        server_list = eval(server_list_file.read())

        for server in server_list:
            if server[0] == check_server.host and server[1] == check_server.port and server[2] == check_server.game:
                return True

        return False


class ServerDownloader(threading.Thread):
    def __init__(self, queue, call_when_server_ready):
        threading.Thread.__init__(self)
        self.queue = queue
        self.call_when_server_ready = call_when_server_ready

    def run(self):
        while True:
            gameserver = self.queue.get()
            self.add_server(gameserver)
            self.queue.task_done()

    def add_server(self, gameserver):
        if gameserver.game == 'Urban Terror':
            UrbanServer(gameserver)
        elif gameserver.game == 'Teeworlds':
            TeeworldsServer(gameserver)
        else:
            return ValueError

        GLib.idle_add(self.call_when_server_ready, gameserver)


def get_masterserver(game):
    if game == 'Urban Terror':
        return UrbanTerrorMaster()
    elif game == 'Teeworlds':
        return TeeworldsMaster()

    return NotImplementedError


class Lists:
    def __init__(self):
        self.call_when_server_created = lambda: None
        self.call_when_server_deleted = lambda: None
        self.call_when_server_updated = lambda: None
        self.masters = 'masters'
        self.q = Queue()

    def lists(self):
        default_servers = [
            ['master.urbanterror.info', 27900, 'Urban Terror']
        ]

        try:
            server_list_file = open(self.masters, 'r')
            server_list = eval(server_list_file.read())
        except FileNotFoundError:
            server_list_file = open(self.masters, 'w')
            server_list_file.write(repr(default_servers))
            server_list_file.close()
            server_list_file = open(self.masters, 'r')
            server_list = eval(server_list_file.read())
        server_list_file.close()

        for _ in range(1):
            t = ListDownloader(self.q, self.call_when_server_created)
            t.setDaemon(True)
            t.start()

        for server in server_list:
            a = ServersList()
            a.host = server[0]
            a.port = server[1]
            a.game = server[2]
            self.q.put(a)

    def add_server(self, hostname, port, game):

        s = get_masterserver(game)
        a = ServersList()
        a.host = hostname
        a.port = port
        a.game = game
        a.servers = s.get_servers(hostname, port, game)

        GLib.idle_add(self.call_when_server_created, a)

    def update_server_data(self, server):
        s = get_masterserver(server.game)
        server.servers = s.get_servers(server.host, server.port, server.game)
        GLib.idle_add(self.call_when_server_updated, server)

    def add_new_list(self, hostname, port, game):

        server_list_file = open(self.masters, 'r')
        server_list = eval(server_list_file.read())
        server_list.append([hostname, port, game])

        server_list_file = open(self.masters, 'w')
        server_list_file.write(repr(server_list))
        server_list_file.close()

        self.add_server(hostname, port, game)


class ListDownloader(threading.Thread):
    def __init__(self, queue, call_when_server_ready):
        threading.Thread.__init__(self)
        self.queue = queue
        self.call_when_server_ready = call_when_server_ready

    def run(self):
        while True:
            masterserver = self.queue.get()
            self.add_server(masterserver)
            self.queue.task_done()

    def add_server(self, masterserver):
        s = get_masterserver(masterserver.game)
        masterserver_servers = s.get_servers(masterserver.host, masterserver.port, masterserver.game)
        masterserver.servers = masterserver_servers

        GLib.idle_add(self.call_when_server_ready, masterserver)
