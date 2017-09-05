import threading
import time

import gi

from monni.ui.server.list_row import ListServerData

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

from ..new_server import NewServer


la = threading.Lock()


class Favorites:

    def __init__(self, win, home, load, page):
        self.win = win
        self.home = home
        self.load = load
        self.page = page

        self.last_servers_update = time.time()

        self.load.call_when_server_created = self.server_created
        self.load.call_when_server_deleted = self.server_deleted
        self.load.call_when_server_updated = self.server_updated

        self.servers = Gtk.ListBox()
        self.servers.set_hexpand(True)
        self.servers.set_vexpand(True)
        self.servers.set_border_width(30)

    def setup(self, stack):
        self.stack = stack

        favorites_grid = Gtk.Grid()
        favorites_grid.set_hexpand(True)
        favorites_grid.set_vexpand(True)

        search = self._search()
        favorites_grid.attach(search, 0, 2, 1, 1)

        servers_window = Gtk.ScrolledWindow()
        servers_window.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        servers_window.set_hexpand(True)
        servers_window.set_vexpand(True)

        self.servers.connect('row-activated', lambda widget, row: row.select_server())

        servers_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        servers_box.pack_start(self.servers, True, True, 0)
        servers_window.add(servers_box)
        favorites_grid.attach(servers_window, 0, 3, 1, 1)

        favorites_down = self._favorites_down()
        favorites_grid.attach(favorites_down, 0, 4, 1, 1)

        stack.add_titled(favorites_grid, "grid", "Favorites")
        self.load.servers()

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
        update_servers_button.connect("clicked", self._update_servers)
        favorites_down.pack_end(update_servers_button, True, True, 0)

        return favorites_down

    def _new_server(self, button):
        NewServer(self.win, self.load)

    def _update_servers(self, button):
        if time.time() - self.last_servers_update < 4:
            return

        for server in self.servers.get_children():
            thread = threading.Thread(target=self._update_server, args=(server,))
            thread.daemon = True
            thread.start()

        self.last_servers_update = time.time()

    def _search(self):
        searchbar = Gtk.SearchBar()
        searchentry = Gtk.SearchEntry()
        searchentry.set_size_request(500,-1)
        searchentry.set_hexpand(True)
        searchbar.set_hexpand(True)

        searchentry.connect("search-changed", self._on_search_changed)
        searchbar.connect_entry(searchentry)
        searchbar.add(searchentry)
        searchbar.set_search_mode(True)

        searchbar.set_valign(Gtk.Align.CENTER)
        searchbar.set_halign(Gtk.Align.CENTER)
        return searchbar

    def _on_search_changed(self, searchentry):
        data = searchentry.get_text()

        def filter_func(row, data, notify_destroy):
            if data is '':
                return True
            if row.game_server.hostname is None:
                return False
            if data in row.game_server.hostname.lower():
                return True
            if data in row.game_server.host.lower():
                return True
            if data in row.game_server.map.lower():
                return True
            return False

        self.servers.set_filter_func(filter_func, data, False)

    def _update_server(self, server):
        server.load.update_server_data(server.game_server)

    def server_created(self, server):
        la.acquire()
        self.servers.add(ListServerData(server, self.win, self.load, self.page, self.home.stack_box, self.home))

        def sort_func(row_1, row_2, data, notify_destroy):
            return len(row_1.game_server.playerlist) < len(row_2.game_server.playerlist)

        self.servers.set_sort_func(sort_func, None, False)
        la.release()

    def server_deleted(self, delete_server):
        la.acquire()
        for server in self.servers:
            if server.game_server == delete_server:
                self.servers.remove(server)
        la.release()

    def server_updated(self, update_server):
        la.acquire()

        for server in self.servers:
            if server.game_server == update_server:
                server.update()

        def sort_func(row_1, row_2, data, notify_destroy):
            return len(row_1.game_server.playerlist) < len(row_2.game_server.playerlist)

        self.servers.set_sort_func(sort_func, None, False)
        la.release()