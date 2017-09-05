import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

from ..server.list_row import ListServerData


class ListPage:

    def __init__(self, win, load, home, page):
        self.win = win
        self.load = load
        self.home = home
        self.data = None
        self.page = page

    def show(self):
        self.setup(self.data)

    def setup(self, data):
        self.data = data

        self.box_outer = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)

        self.win.set_title("%s:%s - Monni" % (self.data.host, self.data.port))

        servers_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)

        self.setup_up_buttons()
        self.setup_servers(servers_box)

        self.box_outer.pack_start(servers_box, True, True, 0)

        self.win.add(self.box_outer)
        self.win.show_all()

    def setup_servers(self, server_box):

        servers_window = Gtk.ScrolledWindow()
        servers_window.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        servers_window.set_hexpand(True)
        servers_window.set_vexpand(True)
        self.server_list = Gtk.ListBox()
        self.server_list.set_border_width(30)
        servers = self.data.servers

        for server in servers:
            self.server_list.add(ListServerData(server, self.win, self.load, self.page, self.box_outer, self))

            def sort_func(row_1, row_2, data, notify_destroy):
                return len(row_1.game_server.playerlist) < len(row_2.game_server.playerlist)

            self.server_list.set_sort_func(sort_func, None, False)

        self.server_list.connect('row-activated', lambda widget, row: row.select_server())
        servers_window.add(self.server_list)

        server_box.pack_end(servers_window, True, True, 0)

    def setup_up_buttons(self):
        button_box = Gtk.Box(spacing=6)

        back_button = Gtk.Button()
        back_button.set_label('Back')
        back_button.connect('clicked', self.back)

        button_box.pack_start(back_button, True, True, 0)

        reload_button = Gtk.Button()
        reload_button.set_label('Update')
        #reload_button.connect('clicked', )

        button_box.pack_end(reload_button, True, True, 0)

        self.box_outer.pack_start(button_box, False, False, 0)

    def back(self, button):
        self.win.remove(self.box_outer)
        self.home.show()
