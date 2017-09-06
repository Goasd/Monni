import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk


class ListServerData(Gtk.ListBoxRow):

    def __init__(self, game_server, win, load, page, previous, back):
        super(Gtk.ListBoxRow, self).__init__()
        self.game_server = game_server
        self.win = win
        self.load = load
        self.page = page
        self.previous = previous
        self.back = back

        self.a = Gtk.Label()
        self.a.set_padding(10,10)
        self.a.set_valign(Gtk.Align.START)
        self.a.set_halign(Gtk.Align.START)
        self.a.set_justify(Gtk.Justification.LEFT)

        self.c = Gtk.Label()
        self.c.set_width_chars(5)
        self.c.set_padding(10, 0)
        self.c.set_line_wrap(True)
        self.c.set_valign(Gtk.Align.CENTER)
        self.c.set_halign(Gtk.Align.END)
        self.c.set_justify(Gtk.Justification.CENTER)

        self.b = Gtk.Label()
        self.b.set_padding(10, 10)
        self.b.set_line_wrap(True)
        self.b.set_valign(Gtk.Align.START)
        self.b.set_halign(Gtk.Align.END)
        self.b.set_justify(Gtk.Justification.RIGHT)

        box_outer = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        grid = Gtk.Grid()
        grid.set_hexpand(True)
        grid.set_vexpand(True)
        grid.set_valign(Gtk.Align.CENTER)
        grid.set_halign(Gtk.Align.END)

        grid.attach(self.b, 0, 0, 1, 1)
        grid.attach(self.c, 1, 0, 1, 1)

        box_outer.pack_start(self.a, True, True, 0)
        box_outer.pack_end(grid, True, True, 0)


        self.add(box_outer)

        self.update()

    def select_server(self):
        self.win.remove(self.previous)
        self.page.setup(self.game_server, self.back, self.load)

    def update(self):
        self.a.set_markup('<span size="x-large">%.30s</span>\n<span>%s:%s</span>' %
                          (
                              self.game_server.hostname,
                              self.game_server.host,
                              self.game_server.port
                          )
                          )
        self.c.set_markup('<span size="x-large">%s</span>\n<span size="small">ms</span>' %
                          (
                              self.game_server.ping
                          )
                          )
        self.b.set_markup('<span size="large">Players %s/%s</span>\n<span>%s</span>' %
                          (
                              self.game_server.players,
                              self.game_server.max_players,
                              self.game_server.map
                          )
                          )