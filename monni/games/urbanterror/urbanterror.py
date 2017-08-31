import socket

import re

from ..server import Server, Connect

SOCKET_TIMEOUT = 3


class UrbanServer(Server):

    def __init__(self, host, port, call_when_server_updated):
        super().__init__(host, port, call_when_server_updated)
        self.game = 'Urban Terror'
        self.server_data = UrbanConnect(self.host, self.port)
        self.update_data()

    def update_data(self):
        try:
            self.server_data.update_status()
        except:
            return

        data = str(self.server_data.data).split("\\n")

        variables = ''
        players = []
        for i in range(1, len(data)):

            is_player = re.compile(r'^(-?)(\d+) (\d+) "(.*)"')
            if is_player.match(data[i]):
                splited_data = data[i].split(' ', 2)
                players.append([splited_data[0], splited_data[1], self.clean_color_code(str(splited_data[2])[1:-1])])
            else:
                variables += str(data[i])

        data = variables.split("\\")[1:]
        self.playerlist = players

        data = list(filter(None, data))

        assert len(data) % 2 == 0
        keys = data[0::2]
        values = data[1::2]

        self.variables = dict(zip(keys, values))
        self.max_players = self.variables['sv_maxclients']
        self.hostname = self.clean_color_code(self.variables['sv_hostname'])
        self.mapname = self.variables['mapname']

        self.call_when_server_updated(self)

    def server_configs(self):
        return self.variables

    def clean_color_code(self, string):
        result = ""
        i = 0
        while i < len(string):
            if string[i] == "^":
                i += 2
            else:
                result += string[i]
                i += 1
        return result


class UrbanConnect(Connect):

    def update_status(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.settimeout(SOCKET_TIMEOUT)
        sock.connect((self.host, self.port))
        sock.send(b'\xFF\xFF\xFF\xFFgetstatus')
        data = sock.recv(8192)
        dataa = data
        data = str(data)
        info = data
        players = []
        for a in data.split('\\n')[2:-1]:
            players.append(a.split(' ', 2))
        info = info.split('\\')
        info = list(filter(None, info))
        self.info = ["\\".join(info[i:i+2]).split('\\') for i in range(0, len(info), 2)][3:-1]
        self.data = dataa

    def update_info(self):
        retries = 2
        while retries > 0:
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                sock.settimeout(SOCKET_TIMEOUT)
                sock.connect((self.host, self.port))
                sock.send(b'\xFF\xFF\xFF\xFFgetinfo')
                data = str(sock.recv(2048))
                retries = 0
            except:
                retries -= 1
        return data

