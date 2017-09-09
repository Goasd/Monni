import socket

import time

from monni.games.player import Player
from monni.games.server import Server, Connect


class TeeworldsServer(Server):

    def __init__(self, gameserver):
        super().__init__(gameserver)
        self.game = 'Teeworlds'
        self.server_data = TeeConnect(self.gameserver.host, self.gameserver.port)
        self.update_data()

    def update_data(self):
        self.server_data.update_status()
        data = self.server_data.data

        if data == None:
            return

        data = data.decode("utf-8").split("\x00")

        self.gameserver.hostname = data[2]
        self.gameserver.map = data[3]
        self.gameserver.gametype = data[4]
        self.gameserver.players = int(data[8])
        self.gameserver.max_players = int(data[9])
        self.gameserver.ping = self.server_data.ping

        for i in range(0, int(data[6])):
            player = Player()
            player.name = data[10 + i * 5]
            player.score = data[10 + i * 5 + 3]
            player.ping = '0'
            self.gameserver.playerlist.append(player)


class TeeConnect(Connect):

    def update_status(self):
        self.data = self.send_and_recv(b'\xff\xff\xff\xff\xff\xff\xff\xff\xff\xffgie3\x00')

    def send_and_recv(self, command):
        retries = 2
        self.ping = '∞'

        while retries > 0:

            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                sock.settimeout(3)
                sock.connect((self.host, int(self.port)))
                connect_start = time.time()
                sock.send(command)
                data = sock.recv(8192)
                connect_recv = time.time()
                data = data[14:]

                self.ping = int(round((connect_recv - connect_start) * 1000))

                return data
            except:
                retries -= 1


        return None
