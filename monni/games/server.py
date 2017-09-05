class Server:

    def __init__(self, gameserver):
        self.gameserver = gameserver

    def update_data(self):
        return NotImplementedError


class Connect:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.info = None

    def get_status(self):
        return self.status

    def get_info(self):
        return self.info

    def update_status(self):
        return NotImplementedError

    def send_command(self, password, command):
        return NotImplementedError


