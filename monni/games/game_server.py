from gi.repository import GLib


class GameServer:

    def __init__(self):
        self.hostname = '-'
        self.host = None
        self.port = None
        self.game = None
        self.players = -1
        self.max_players = -1
        self.map = None
        self.variables = {}
        self.playerlist = []
        self.gametype = None

        self.admin_password = ''
        self.server_password = ''

        self.ping = None

        self.sources = []

    def call_update(self):
        print(self.host)
        for source in self.sources:
            GLib.idle_add(source, self)