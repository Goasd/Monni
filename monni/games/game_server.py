class GameServer:

    def __init__(self):
        self.hostname = None
        self.host = None
        self.port = None
        self.game = None
        self.players = -1
        self.max_players = -1
        self.map = None
        self.variables = {}
        self.playerlist = []
        self.gametype = None

        self.admin_password = None
        self.server_password = None

