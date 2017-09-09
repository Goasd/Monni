import socket

from monni.games.game_server import GameServer


class TeeworldsMaster:
    def __init__(self):
        pass

    def get_servers(self, server, port, game):

        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.settimeout(3)

        try:
            sock.connect((server, port))
            sock.send(b'\x20\x00\x00\x00\x00\x00\xff\xff\xff\xffreq2')
        except:
            return []

        servers = []
        while True:
            try:
                data = sock.recv(8000)
            except:
                break

            data = data[14:]

            num_servers = int(len(data) / 18)

            for i in range(0, num_servers):

                ip = socket.inet_ntop(socket.AF_INET, data[i * 18 + 12:i * 18 + 16])

                port = 256 * data[i * 18 + 16] + data[i * 18 + 17]

                gameserver = GameServer()
                gameserver.host = str(ip)
                gameserver.port = int(port)
                gameserver.game = game
                servers.append(gameserver)

        return servers


