import os

from gi.repository import Gtk


class ListPlayerData(Gtk.ListBoxRow):

    def __init__(self, player):
        super(Gtk.ListBoxRow, self).__init__()
        self.player = player
        self.setup_row()

    def setup_row(self):
        row = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        row.set_hexpand(False)
        row.set_vexpand(False)
        data_label = Gtk.Label()
        data_label.set_text(self.player.score)
        data_label.set_width_chars(5)
        data_label.set_valign(Gtk.Align.START)
        data_label.set_halign(Gtk.Align.START)
        data_label.set_justify(Gtk.Justification.LEFT)

        row.pack_start(data_label, True, True, 0)
        data_label = Gtk.Label()
        data_label.set_text(self.player.ping)
        data_label.set_width_chars(5)
        data_label.set_valign(Gtk.Align.START)
        data_label.set_halign(Gtk.Align.CENTER)
        data_label.set_justify(Gtk.Justification.LEFT)

        row.pack_start(data_label, True, True, 0)
        data_label = Gtk.Label()
        data_label.set_text(self.player.name)
        data_label.set_width_chars(20)
        data_label.set_valign(Gtk.Align.START)
        data_label.set_halign(Gtk.Align.END)
        data_label.set_justify(Gtk.Justification.LEFT)

        row.pack_start(data_label, True, True, 0)
        self.add(row)

    def select_player(self):
        print(self.player.name)

class ServerPage:

    def __init__(self, win, load, home):
        self.win = win
        self.load = load
        self.home = home
        self.data = None

    def setup(self, data):
        self.data = data

        self.box_outer = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)

        self.win.set_title("%s - Monni" % self.data.hostname)

        notebook = Gtk.Notebook()
        box_notebook = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)

        self.setup_up_buttons()

        self.setup_players(notebook)

        self.setup_config(notebook)

        box_notebook.pack_start(notebook, True, True, 0)

        self.box_outer.pack_start(box_notebook, True, True, 0)

        self.setup_down_buttons()
        self.win.add(self.box_outer)
        self.win.show_all()

    def setup_players(self, notebook):

        players_notebook = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        players_notebook.set_border_width(10)

        notebook.append_page(players_notebook, Gtk.Label('Players'))

        players_window = Gtk.ScrolledWindow()
        players_window.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        players_window.set_hexpand(True)
        players_window.set_vexpand(True)
        self.players_list = Gtk.ListBox()
        self.players_list.set_border_width(30)
        players = self.data.playerlist

        for player in players:
            self.players_list.add(ListPlayerData(player))

        self.players_list.connect('row-activated', lambda widget, row: row.select_server())
        players_window.add(self.players_list)
        r = self.setup_colum_names()
        players_notebook.pack_start(r, False, False, 0)
        players_notebook.pack_end(players_window, True, True, 0)

    def setup_config(self, notebook):

        config_notebook = Gtk.Box()
        config_notebook.set_border_width(10)

        notebook.append_page(config_notebook, Gtk.Label('Config'))

        config_window = Gtk.ScrolledWindow()
        config_window.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        configsbox = Gtk.ListBox()
        configsbox.set_border_width(30)
        configsbox.set_hexpand(True)
        configsbox.set_vexpand(True)
        configs = self.data.variables
        for key, value in configs.items():
            conf_row = Gtk.Box()

            a = Gtk.Label()
            a.set_padding(10, 10)
            a.set_markup("%s" % (key))
            a.set_valign(Gtk.Align.START)
            a.set_halign(Gtk.Align.START)
            conf_row.pack_start(a, True, True, 0)

            b = Gtk.Label()
            b.set_padding(10, 10)
            b.set_markup("%s" % (value))
            b.set_halign(Gtk.Align.END)
            conf_row.pack_end(b, True, True, 0)

            configsbox.add(conf_row)

        config_window.add(configsbox)

        config_notebook.add(config_window)

    def setup_up_buttons(self):
        button_box = Gtk.Box(spacing=6)

        back_button = Gtk.Button()
        back_button.set_label('Back')
        back_button.connect('clicked', self.back)

        button_box.pack_start(back_button, True, True, 0)

        reload_button = Gtk.Button()
        reload_button.set_label('Update')
        reload_button.connect('clicked', self.reload_data)

        button_box.pack_end(reload_button, True, True, 0)

        self.box_outer.pack_start(button_box, False, False, 0)

    def setup_down_buttons(self):
        button_box = Gtk.Box(spacing=6)

        delete_button = Gtk.Button()
        delete_button.set_label('Delete server')
        delete_button.connect('clicked', self.delete_server)

        button_box.pack_start(delete_button, True, True, 0)

        play_button = Gtk.Button()
        play_button.set_label('Play')
        play_button.connect('clicked', self.play_button)

        button_box.pack_start(play_button, True, True, 0)

        self.box_outer.pack_end(button_box, False, False, 0)

    def setup_colum_names(self):
        row = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        row.set_hexpand(False)
        row.set_vexpand(False)
        self.setup_colum('Score', self.order_by_score, row, 5, Gtk.Align.START)
        self.setup_colum('Ping', self.order_by_ping, row, 5, Gtk.Align.CENTER)
        self.setup_colum('Player', self.order_by_name, row, 20, Gtk.Align.END)
        return row

    def setup_colum(self, name, action_method, row, lenght, align):

        a = Gtk.EventBox()
        data1_label = Gtk.Label()
        data1_label.set_text(name)
        data1_label.set_width_chars(lenght)
        data1_label.set_valign(Gtk.Align.START)
        data1_label.set_halign(align)
        data1_label.set_justify(Gtk.Justification.LEFT)
        a.connect('button-press-event', action_method)
        a.add(data1_label)
        row.pack_start(a, True, True, 0)

    def order_by_score(self, button, b):

        def sort_func(row_1, row_2, data, notify_destroy):
            return int(row_1.player.score) < int(row_2.player.score)

        self.players_list.set_sort_func(sort_func, None, False)

    def order_by_ping(self, button, b):

        def sort_func(row_1, row_2, data, notify_destroy):
            return int(row_1.player.ping) > int(row_2.player.ping)

        self.players_list.set_sort_func(sort_func, None, False)

    def order_by_name(self, button, b):

        def sort_func(row_1, row_2, data, notify_destroy):
            return row_1.player.name > row_2.player.name

        self.players_list.set_sort_func(sort_func, None, False)

    def back(self, button):
        self.win.remove(self.box_outer)
        self.home.show_home()

    def reload_data(self, button):
        self.load.update_server_data(self.data)
        self.win.remove(self.box_outer)
        self.setup(self.data)

    def delete_server(self, button):
        self.load.delete_server(self.data)
        self.back(None)

    def play_button(self, button):
        location = self.load.settings_get_game_location(self.data.game)
        os.system('%s +connect %s:%s &' % (location, self.data.host, self.data.port))
