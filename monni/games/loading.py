import threading
import configparser

from gi.repository import GLib

from .serverslist import ServersList
from .urbanterror.master import Master
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
        config[str(game)] = {}
        config[str(game)]['location'] = location
        with open(self.file, 'w') as configfile:
            config.write(configfile)

    def get_game_location(self, game):
        config = configparser.ConfigParser()
        config.read(self.file)
        return config[game]['location']

class Servers:

    def __init__(self):
        self.call_when_server_created = lambda: None
        self.call_when_server_deleted = lambda: None
        self.call_when_server_updated = lambda: None
        self.file = 'servers'

    def update_server_data(self, server):

        if server.game == 'Urban Terror':
            UrbanServer(server)
        else:
            return ValueError

        GLib.idle_add(self.call_when_server_updated, server)

    def servers_add(self, server_list):

        for server in server_list:
            thread = threading.Thread(target=self.add_server, args=(server.host, server.port, server.game,))
            thread.daemon = True
            thread.start()

    def servers(self):

        default_servers = [
            ['151.80.41.55', 27960, 'Urban Terror']
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

        for server in server_list:
            thread = threading.Thread(target=self.add_server, args=(server[0], server[1], server[2],))
            thread.daemon = True
            thread.start()

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
        server_list.append([hostname, port, game])

        server_list_file = open(self.file, 'w')
        server_list_file.write(repr(server_list))
        server_list_file.close()

        self.add_server(hostname, port, game)

    def delete_server(self, server):
        server_list_file = open(self.file, 'r')
        server_list = eval(server_list_file.read())

        server_list.remove([server.host, server.port, server.game])

        server_list_file = open(self.file, 'w')
        server_list_file.write(repr(server_list))
        server_list_file.close()

        GLib.idle_add(self.call_when_server_deleted, server)

    def add_list(self, hostname, port, game):
        pass

    def add_new_list(self, hostname, port, game):

        server_list_file = open(self.masters, 'r')
        server_list = eval(server_list_file.read())
        server_list.append([hostname, port, game])

        server_list_file = open(self.masters, 'w')
        server_list_file.write(repr(server_list))
        server_list_file.close()

        self.add_list(hostname, port, game)


class Lists:

    def __init__(self):
        self.call_when_server_created = lambda: None
        self.call_when_server_deleted = lambda: None
        self.call_when_server_updated = lambda: None
        self.masters = 'masters'

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

        for server in server_list:
            thread = threading.Thread(target=self.add_server, args=(server[0], server[1], server[2],))
            thread.daemon = True
            thread.start()

    def add_server(self, hostname, port, game):

        s = Master()
        a = ServersList()
        a.host = hostname
        a.port = port
        a.game = game
        a.servers = s.get_servers(hostname, port, game)

        GLib.idle_add(self.call_when_server_created, a)

    def update_server_data(self, server):
        s = Master()
        server.servers = s.get_servers(server.host, server.port, server.game)
        GLib.idle_add(self.call_when_server_updated, server)