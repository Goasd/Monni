import threading
import configparser

from .list import List
from .urbanterror.master import Master
from .game_server import GameServer
from .urbanterror.urbanterror import UrbanServer

l = threading.Lock()
servers = []


class Load:

    def __init__(self):
        self.call_when_server_created = lambda: None
        self.call_when_server_deleted = lambda: None
        self.call_when_server_updated = lambda: None
        self.file = 'servers'

    def settings(self):
        config = configparser.ConfigParser()
        config.read("config.ini")
        print(config)

    def settings_set_game_location(self, game, location):
        config = configparser.ConfigParser()
        config[str(game)] = {}
        config[str(game)]['location'] = location
        with open('config.ini', 'w') as configfile:
            config.write(configfile)

    def settings_get_game_location(self, game):
        config = configparser.ConfigParser()
        config.read("config.ini")
        return config[game]['location']

    def lists(self):
        l = []
        a = List()
        a.url = 'master.urbanterror.info'
        a.host = 'master.urbanterror.info'
        a.port = 27900
        a.game = 'Urban Terror'
        a.servers = self.servers_in_list()
        l.append(a)
        return l

    def servers_in_list(self):

        s = Master()
        return s.get_servers()

    def update_server_data(self, server):

        if server.game == 'Urban Terror':
            UrbanServer(server)
        else:
            return ValueError

        self.call_when_server_updated(server)

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

        threads = []
        for server in server_list:
            thread = threading.Thread(target=self.add_server, args=(server[0], server[1], server[2],))
            thread.daemon = True
            thread.start()
            threads.append(thread)

        for thread in threads:
            thread.join()

    def add_server(self, hostname, port, game):

        gameserver = GameServer()
        gameserver.game = game
        gameserver.port = port
        gameserver.host = hostname

        if game == 'Urban Terror':
            UrbanServer(gameserver)
        else:
            return ValueError

        self.call_when_server_created(gameserver)

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

        self.call_when_server_deleted(server)

