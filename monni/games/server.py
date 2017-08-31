class Server:

    def __init__(self, host, port, call_when_server_updated):
        self.host = host
        self.port = int(port)
        self.call_when_server_updated = call_when_server_updated
        self.game = None
        self.hostname = None
        self.variables = {}

        self.playerlist = []
        self.max_players = None
        self.mapname = None
        self.gametype = None

        self.admin_password = None
        self.server_password = None

    def update_data(self):
        return NotImplementedError

    def get_players(self):
        return self.playerlist

    def server_configs(self):
        return NotImplementedError

    def get_players_online(self):
        return len(self.playerlist)

    def get_players_max(self):
        return self.max_players


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


