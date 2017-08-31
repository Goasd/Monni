import threading
import configparser

from ..games.urbanterror.urbanterror import UrbanServer

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

    def servers(self):

        default_servers = [
            ['151.80.41.55', 27960, 'urbanterror']
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

        if game == 'Urban Terror':
            new_server = UrbanServer(hostname, port, self.call_when_server_updated)
        else:
            return ValueError

        servers.append(new_server)
        self.call_when_server_created(new_server)

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
        print(server_list)
        print(server)
        server_list.remove([server.host, server.port, server.game])

        server_list_file = open(self.file, 'w')
        server_list_file.write(repr(server_list))
        server_list_file.close()

        servers.remove(server)
        self.call_when_server_deleted(server)

