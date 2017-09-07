import gi

from monni.games import loading
from monni.games.loading import Lists

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

from ..servers import Servers
from .new_server import NewServer


class Favorites:

    def __init__(self, win, home, page):
        self.win = win
        self.home = home
        self.load_servers = loading.Servers()
        self.page = page

    def setup(self, stack):
        self.servers_ui = Servers(self.win, self.home, self.load_servers, self.page, self.home.stack_box, self.home)
        favorites_grid = Gtk.Grid()
        favorites_grid.set_hexpand(True)
        favorites_grid.set_vexpand(True)
        self.servers_ui.setup(favorites_grid, self.load_servers.servers)

        favorites_down = self._favorites_down()
        favorites_grid.attach(favorites_down, 0, 4, 1, 1)

        stack.add_titled(favorites_grid, "grid", "Favorites")

    def _favorites_down(self):
        favorites_down = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)

        new_server_button = Gtk.Button()
        new_server_button.set_relief(Gtk.ReliefStyle.NONE)
        new_server_button.set_label('New server')
        new_server_button.connect("clicked", self._new_server)
        favorites_down.pack_start(new_server_button, True, True, 0)

        update_servers_button = Gtk.Button()
        update_servers_button.set_relief(Gtk.ReliefStyle.NONE)
        update_servers_button.set_label('Update servers')
        update_servers_button.connect("clicked", self.servers_ui._update_servers)
        favorites_down.pack_end(update_servers_button, True, True, 0)

        return favorites_down

    def _new_server(self, button):
        NewServer(self.win, self.load)
