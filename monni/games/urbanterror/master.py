import socket

from ..game_server import GameServer


class Master:
    def __init__(self):
        pass

    def get_servers(self, server, port, game):

        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.settimeout(3)
        sock.connect((server, port))
        sock.send(b'\xFF\xFF\xFF\xFFgetservers 68 empty full')
        l = []
        while True:
            try:
                data = sock.recv(2000)[22:]
                l.append(data)
            except:
                break

        servers = []
        for packet in l:

            i = 0
            while True:
                if i + 7 >= len(packet):
                    break
                ip = socket.inet_ntop(socket.AF_INET, packet[i + 1:i + 5])
                port = 256 * packet[i + 5] + packet[i + 6]
                gameserver = GameServer()
                gameserver.host = str(ip)
                gameserver.port = int(port)
                gameserver.game = game
                servers.append(gameserver)
                i += 7
        return servers


