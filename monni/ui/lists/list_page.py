from gi.repository import Gtk

from monni.games import loading
from monni.ui.servers import Servers


class ListPage:

    def __init__(self, win, home, page, load):
        self.win = win
        self.load = load
        self.home = home
        self.data = None
        self.page = page
        self.box_outer = None
        self.box_outer = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        self.servers_ui = Servers(self.win, self.home, self.load, self.page, self.box_outer, self)

    def show(self, data=None):
        if data is not None:
            self.setup(data)
        else:
            self.win.add(self.box_outer)
        self.win.set_title("%s:%s - Monni" % (self.data.host, self.data.port))

    def show_back(self, data=None):
        self.win.add(self.box_outer)
        self.win.set_title("%s:%s - Monni" % (self.data.host, self.data.port))

    def setup(self, data):
        if self.data is None:
            self.data = data
            servers_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)

            self.setup_up_buttons()

            servers_grid = Gtk.Grid()
            servers_grid.set_hexpand(True)
            servers_grid.set_vexpand(True)
            self.servers_ui.setup(servers_grid, self.server_data)
            servers_box.add(servers_grid)

            self.box_outer.pack_start(servers_box, True, True, 0)

        self.win.add(self.box_outer)
        self.win.show_all()

    def server_data(self, a):
        return self.load.servers_add(self.data.servers, a)

    def setup_up_buttons(self):
        button_box = Gtk.Box(spacing=6)

        back_button = Gtk.Button()
        back_button.set_label('Back')
        back_button.connect('clicked', self.back)

        button_box.pack_start(back_button, True, True, 0)

        reload_button = Gtk.Button()
        reload_button.set_label('Update')
        reload_button.connect('clicked', self.servers_ui._update_servers)

        button_box.pack_end(reload_button, True, True, 0)

        self.box_outer.pack_start(button_box, False, False, 0)

    def back(self, button):
        self.win.remove(self.box_outer)
        self.home.show()
