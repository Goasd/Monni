import threading
import configparser
from queue import Queue

import multiprocessing
from gi.repository import GLib

from monni.games.teeworlds.console import TeeworldsConsole
from monni.games.teeworlds.master import TeeworldsMaster
from monni.games.teeworlds.teeworlds import TeeworldsServer

from monni.games.urbanterror.console import UrbanTerrorConsole
from .serverslist import ServersList
from .urbanterror.master import UrbanTerrorMaster
from .game_server import GameServer
from .urbanterror.urbanterror import UrbanServer


class Console:
    def __init__(self, gameserver):
        self.gameserver = gameserver
        if self.gameserver.game == 'Urban Terror':
            self.console = UrbanTerrorConsole(self.gameserver)
        elif self.gameserver.game == 'Teeworlds':
            self.console = TeeworldsConsole(self.gameserver)

    def send_command(self, password, command):
        return self.console.send_command(password, command)

    def support(self):
        return self.console.support()


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


class Load:
    def __init__(self):
        self.servers = []

        self.call_when_server_created = lambda: None
        self.call_when_server_deleted = lambda: None
        self.call_when_server_updated = lambda: None

        self.call_when_list_created = lambda: None
        self.call_when_list_deleted = lambda: None
        self.call_when_list_updated = lambda: None

        self.masters = Lists()
        self.masters.server_add = self.servers_add_new

        self.masters.call_when_server_created = self.call_when_list_created
        self.masters.call_when_server_deleted = self.call_when_list_deleted
        self.masters.call_when_server_updated = self.call_when_list_updated

        self.file = 'servers'
        self.q = Queue()
        self.settings = Settings()

    def get_master_servers(self):
        p = multiprocessing.Process(target=self.masters.lists())
        p.daemon = True
        p.start()

    def update_server_data(self, server):
        for _ in range(1):
            t = ServerDownloader(self.q, None)
            t.setDaemon(True)
            t.start()
        self.q.put(server)

    def servers_add(self, server_list):

        for _ in range(3):
            t = ServerDownloader(self.q, self.call_when_server_created)
            t.setDaemon(True)
            t.start()

        for server in server_list:
            self.q.put(server)

    def get_servers(self):

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
            gameserver = self.servers_add_new(server[0], server[1], server[2], self.call_when_server_updated)
            q.put(gameserver)

    def add_server(self, hostname, port, game):

        gameserver = self.servers_add_new(hostname, port, game, self.call_when_server_updated)

        GLib.idle_add(self.call_when_server_created, gameserver)

        if game == 'Urban Terror':
            UrbanServer(gameserver)
        elif game == 'Teeworlds':
            TeeworldsServer(gameserver)
        else:
            return ValueError

    def servers_add_new(self, host, port, game, call_method=None):

        server = [x for x in self.servers if x.host == host and x.port == port and x.game == game]
        if len(server) > 0:
            server = server[0]
            if call_method is not None:
                server.add_call_update_method(call_method)
            else:
                server.add_call_update_method(self.call_when_server_updated)
            return server

        gameserver = GameServer()
        gameserver.game = game
        gameserver.port = port
        gameserver.host = host
        if call_method is not None:
            gameserver.add_call_update_method(call_method)
        else:
            gameserver.add_call_update_method(self.call_when_server_updated)
        self.servers.append(gameserver)
        return gameserver

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

        s = [x for x in server_list if x[0] == server.host and x[1] == server.port and x[2] == server.game]
        if len(s) > 0:
            s = s[0]
            server_list.remove(s)

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
        if self.call_when_server_ready is not None:
            GLib.idle_add(self.call_when_server_ready, gameserver)
        gameserver.call_update()


def get_masterserver(game):
    if game == 'Urban Terror':
        return UrbanTerrorMaster()
    elif game == 'Teeworlds':
        return TeeworldsMaster()

    return NotImplementedError


class Lists:
    def __init__(self):
        self.servers = []
        self.call_when_server_created = lambda: None
        self.call_when_server_deleted = lambda: None
        self.call_when_server_updated = lambda: None
        self.server_add = None

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

        for _ in range(3):
            t = ListDownloader(self.q, self.call_when_server_created, self.server_add)
            t.setDaemon(True)
            t.start()

        for server in server_list:
            a = ServersList()
            a.host = server[0]
            a.port = server[1]
            a.game = server[2]
            a.add_call_update_method(self.call_when_server_updated)
            self.q.put(a)
            self.servers.append(a)

    def add_server(self, hostname, port, game):

        s = get_masterserver(game)
        a = ServersList()
        a.host = hostname
        a.port = port
        a.game = game
        self.servers.append(a)
        a.servers = s.get_servers(hostname, port, game, self.server_add)
        GLib.idle_add(self.call_when_server_created, a)

    def update_server_data(self, server):
        s = get_masterserver(server.game)
        server.servers = s.get_servers(server.host, server.port, server.game, self.server_add)
        server.call_update()

    def add_new_list(self, hostname, port, game):

        server_list_file = open(self.masters, 'r')
        server_list = eval(server_list_file.read())
        server_list.append([hostname, port, game])

        server_list_file = open(self.masters, 'w')
        server_list_file.write(repr(server_list))
        server_list_file.close()

        self.add_server(hostname, port, game)


class ListDownloader(threading.Thread):
    def __init__(self, queue, call_when_server_ready, servers_add):
        threading.Thread.__init__(self)
        self.queue = queue
        self.call_when_server_ready = call_when_server_ready
        self.servers_add = servers_add

    def run(self):
        while True:
            masterserver = self.queue.get()
            self.add_server(masterserver)
            self.queue.task_done()

    def add_server(self, masterserver):
        s = get_masterserver(masterserver.game)
        masterserver_servers = s.get_servers(masterserver.host, masterserver.port, masterserver.game, self.servers_add)
        masterserver.servers = masterserver_servers

        GLib.idle_add(self.call_when_server_ready, masterserver)
