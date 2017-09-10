from monni.games.urbanterror.urbanterror import UrbanConnect


class UrbanTerrorConsole:
    def __init__(self, gameserver):
        self.gameserver = gameserver
        self.a = UrbanConnect(self.gameserver.host, self.gameserver.port)

    def send_command(self, password, command):
        rcon_command = 'rcon %s %s' % (password, command)
        data = self.a.send_and_recv(rcon_command)
        data = data[9:-1]
        data = str(data, 'utf-8')
        data = data.split('\\n')
        return data

    def support(self):
        return True