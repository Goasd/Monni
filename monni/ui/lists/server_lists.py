import threading
import time

import gi

from monni.ui.lists.list_page import ListPage

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk


la = threading.Lock()

class ListData(Gtk.ListBoxRow):

    def __init__(self, game_server, win, load, home, page):
        super(Gtk.ListBoxRow, self).__init__()
        self.server_list = game_server
        self.win = win
        self.load = load
        self.home = home
        self.page = page

        self.a = Gtk.Label()
        self.a.set_padding(10,10)
        self.a.set_line_wrap(True)
        self.a.set_valign(Gtk.Align.START)
        self.a.set_halign(Gtk.Align.START)
        self.a.set_justify(Gtk.Justification.LEFT)

        self.b = Gtk.Label()
        self.b.set_padding(10, 10)
        self.b.set_line_wrap(True)
        self.b.set_valign(Gtk.Align.START)
        self.b.set_halign(Gtk.Align.END)
        self.b.set_justify(Gtk.Justification.RIGHT)

        box_outer = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        box_outer.pack_start(self.a, True, True, 0)
        box_outer.pack_end(self.b, True, True, 0)

        self.add(box_outer)

        self.update()

    def select_server(self):
        self.win.remove(self.home.stack_box)
        self.page.setup(self.server_list)

    def update(self):
        self.a.set_markup('<span size="x-large">%s:%s</span>\n<span>%s</span>' %
                          (
                              self.server_list.host,
                              self.server_list.port,
                              self.server_list.game
                          )
                          )
        self.b.set_markup('<span size="large">Servers %s</span>\n<span></span>' %
                          (
                              len(self.server_list.servers)
                          )
                          )


class ServerLists:

    def __init__(self, win, home, load):
        self.win = win
        self.home = home
        self.load = load
        self.page = ListPage(self.win, self.load, self.home)

        self.last_servers_update = time.time()

        self.servers = Gtk.ListBox()
        self.servers.set_hexpand(True)
        self.servers.set_vexpand(True)
        self.servers.set_border_width(30)

    def setup(self, stack):

        server_lists_grid = Gtk.Grid()
        server_lists_grid.set_hexpand(True)
        server_lists_grid.set_vexpand(True)

        servers_window = Gtk.ScrolledWindow()
        servers_window.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        servers_window.set_hexpand(True)
        servers_window.set_vexpand(True)

        self.servers.connect('row-activated', lambda widget, row: row.select_server())

        servers_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        servers_box.pack_start(self.servers, True, True, 0)
        servers_window.add(servers_box)
        server_lists_grid.attach(servers_window, 0, 3, 1, 1)

        favorites_down = self._lists_down()
        server_lists_grid.attach(favorites_down, 0, 4, 1, 1)

        stack.add_titled(server_lists_grid, "label", "Server lists")
        self.servers.show_all()
        thread = threading.Thread(target=self.lists, args=())
        thread.daemon = True
        thread.start()

    def lists(self):
        b = self.load.lists()
        for a in b:
            la.acquire()
            self.servers.add(ListData(a, self.win, self.load, self.home, self.page))
            self.servers.show_all()
            la.release()
            for s in a.servers:
                thread = threading.Thread(target=self.load.update_server_data, args=(s,))
                thread.daemon = True
                thread.start()

    def servers(self):
        self.load.servers_in_list()

    def _lists_down(self):
        lists_down = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)

        new_list_button = Gtk.Button()
        new_list_button.set_relief(Gtk.ReliefStyle.NONE)
        new_list_button.set_label('New list')
        #new_list_button.connect("clicked", )
        lists_down.pack_start(new_list_button, True, True, 0)

        update_lists_button = Gtk.Button()
        update_lists_button.set_relief(Gtk.ReliefStyle.NONE)
        update_lists_button.set_label('Update lists')
        #update_lists_button.connect("clicked", )
        lists_down.pack_end(update_lists_button, True, True, 0)

        return lists_down


