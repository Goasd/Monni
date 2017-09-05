import html
import socket

import re

import time

from ..player import Player
from ..server import Server, Connect

SOCKET_TIMEOUT = 3


class UrbanServer(Server):

    def __init__(self, gameserver):
        super().__init__(gameserver)
        self.game = 'Urban Terror'
        self.server_data = UrbanConnect(self.gameserver.host, self.gameserver.port)
        self.update_data()

    def update_data(self):
        try:
            self.server_data.update_status()
        except:
            return
        data = self.server_data.data
        data = data.decode("latin-1").split("\n")

        variables = ''
        players = []
        for i in range(0, len(data)):

            is_player = re.compile(r'^(-?)(\d+) (\d+) "(.*)"')
            if is_player.match(data[i]):
                player_data = data[i].split(' ', 2)
                player = Player()
                player.name = self.clean_color_code(str(player_data[2]))[1:-1]
                player.ping = player_data[1]
                player.score = player_data[0]
                players.append(player)
            else:
                variables += data[i]

        self.gameserver.playerlist = players
        data = variables.split("\\")[1:]
        data = list(filter(None, data))

        assert len(data) % 2 == 0

        keys = data[0::2]
        values = data[1::2]

        variables = dict(zip(keys, values))
        self.gameserver.max_players = variables['sv_maxclients']
        self.gameserver.players = len(players)
        self.gameserver.hostname = html.escape(self.clean_color_code(variables['sv_hostname']))
        self.gameserver.variables = variables
        self.gameserver.map = variables['mapname']
        self.gameserver.ping = self.server_data.ping


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
        connect_start = time.time()
        sock.send(b'\xFF\xFF\xFF\xFFgetstatus')
        data = sock.recv(8192)[19:-1]
        connect_recv = time.time()
        self.ping = int(round((connect_recv - connect_start) * 1000))
        dataa = data
        data = str(data)
        info = data
        players = []
        for a in data.split('\\n'):
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

    def send_command(self, password, command):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.settimeout(SOCKET_TIMEOUT)
        sock.connect((self.host, self.port))
        rcon_command = str.encode('rcon %s %s' % (password, command))
        sock.send(b'\xFF\xFF\xFF\xFF'+rcon_command)
        data = sock.recv(2048)
        data = data[9:-1]
        data = str(data,'utf-8')
        data = data.split('\\n')
        return data

