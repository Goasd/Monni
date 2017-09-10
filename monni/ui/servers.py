import threading

import time
from gi.repository import Gtk

from ..ui.server.list_row import ListServerData


class Servers:

    def __init__(self, win, home, load, page, prev, back):
        self.win = win
        self.home = home
        self.load = load
        self.page = page
        self.prev = prev
        self.back = back

        self.load.call_when_server_created = self.server_created
        self.load.call_when_server_deleted = self.server_deleted
        self.load.call_when_server_updated = self.server_updated

        self.servers = Gtk.ListBox()
        self.servers.set_hexpand(True)
        self.servers.set_vexpand(True)
        self.servers.set_border_width(30)

        self.last_servers_update = time.time()

    def setup(self, grid, servers):

        search = self._search()
        grid.attach(search, 0, 2, 1, 1)

        servers_window = Gtk.ScrolledWindow()
        servers_window.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        servers_window.set_hexpand(True)
        servers_window.set_vexpand(True)

        self.servers.connect('row-activated', lambda widget, row: row.select_server())

        servers_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        servers_box.pack_start(self.servers, True, True, 0)
        servers_window.add(servers_box)
        grid.attach(servers_window, 0, 3, 1, 1)

        thread = threading.Thread(target=servers())
        thread.daemon = True
        thread.start()

    def _update_servers(self, button):
        if time.time() - self.last_servers_update > 2:

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
        self.servers.add(ListServerData(server, self.win, self.load, self.page, self.prev, self.back))

        def sort_func(row_1, row_2, data, notify_destroy):
            return row_1.game_server.players < row_2.game_server.players

        self.servers.set_sort_func(sort_func, None, False)
        self.servers.show_all()

    def server_deleted(self, delete_server):
        for server in self.servers:
            if server.game_server == delete_server:
                self.servers.remove(server)

    def server_updated(self, update_server):

        for server in self.servers:
            if server.game_server == update_server:
                server.update()

        def sort_func(row_1, row_2, data, notify_destroy):
            return row_1.game_server.players < row_2.game_server.players

        self.servers.set_sort_func(sort_func, None, False)