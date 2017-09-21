import copy
from gi.repository import GLib


class ServersList:
    def __init__(self):
        self.url = None
        self.host = None
        self.port = None
        self.servers = []
        self.game = None

        self.sources = []
        self.call_game_server_update_method = None

    def call_update(self):
        for source in self.sources:
            GLib.idle_add(source, self)

    def add_call_update_method(self, method):
        self.sources.append(copy.copy(method))
