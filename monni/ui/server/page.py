import html
import os
from gi.repository import Gtk

from monni.games import loading
from monni.games.urbanterror.urbanterror import UrbanConnect
from monni.ui.server.player_info import PlayerInfo


class ListPlayerData(Gtk.ListBoxRow):

    def __init__(self, player, win):
        super(Gtk.ListBoxRow, self).__init__()
        self.player = player
        self.win = win
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
        PlayerInfo(self.win).setup(self.player)


class ServerPage:

    def __init__(self, win, home):
        self.win = win
        self.load = None
        self.home = home
        self.data = None
        self.settings = loading.Settings()

    def setup(self, data, back, load):
        self.data = data
        self.backa = back
        self.load = load

        self.box_outer = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        self.win.set_title("%s - Monni" % self.data.hostname)

        notebook = Gtk.Notebook()
        box_notebook = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)

        self.setup_up_buttons()

        self.setup_info(notebook)

        self.setup_players(notebook)

        self.setup_config(notebook)

        self.setup_console(notebook)

        self.setup_passwords(notebook)

        box_notebook.pack_start(notebook, True, True, 0)

        self.box_outer.pack_start(box_notebook, True, True, 0)

        self.setup_down_buttons()
        self.win.add(self.box_outer)
        self.win.show_all()

    def setup_passwords(self, notebook):
        info_notebook = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        info_notebook.set_border_width(10)

        notebook.append_page(info_notebook, Gtk.Label('Passwords'))

        info_window = Gtk.ScrolledWindow()
        info_window.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)

        box_vertical = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)

        admin_password_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)

        label_admin_password = Gtk.Label()
        label_admin_password.set_text('Admin password')

        self.text_password = Gtk.Entry()
        self.text_password.set_text(self.settings.get_admin_password(self.data))
        admin_save_button = Gtk.Button()
        admin_save_button.set_label("Save")
        admin_save_button.connect('clicked', self.save_password, self.text_password.get_text)

        admin_password_box.pack_start(self.text_password, True, True, 0)
        admin_password_box.pack_end(admin_save_button, False, True, 0)

        box_vertical.pack_start(label_admin_password, False, False, 0)
        box_vertical.pack_start(admin_password_box, False, False, 0)

        admin_password_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)

        label_server_password = Gtk.Label()
        label_server_password.set_text('Server password')

        self.text_server_password = Gtk.Entry()
        self.text_server_password.set_text(self.settings.get_server_password(self.data))
        admin_save_button = Gtk.Button()
        admin_save_button.set_label("Save")
        admin_save_button.connect('clicked', self.save_server_password, self.text_server_password.get_text)

        admin_password_box.pack_start(self.text_server_password, True, True, 0)
        admin_password_box.pack_end(admin_save_button, False, True, 0)

        box_vertical.pack_start(label_server_password, False, False, 0)
        box_vertical.pack_start(admin_password_box, False, False, 0)

        info_notebook.pack_end(box_vertical, True, True, 0)

    def save_password(self, button, password):
        self.data.admin_password = password()
        self.settings.set_admin_password(self.data, self.data.admin_password)

    def save_server_password(self, button, password):
        self.data.server_password = password()
        self.settings.set_server_password(self.data, self.data.server_password)

    def setup_console(self, notebook):
        info_notebook = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        info_notebook.set_border_width(10)

        notebook.append_page(info_notebook, Gtk.Label('Console'))

        info_window = Gtk.ScrolledWindow()
        info_window.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)

        box_vertical = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)

        self.command_history_buffer = Gtk.TextBuffer()
        self.command_history = Gtk.TextView(buffer=self.command_history_buffer)

        box_command = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)

        self.text_command = Gtk.Entry()
        send_button = Gtk.Button()
        send_button.set_label("Send")
        send_button.connect('clicked', self.send_command, self.text_command.get_text)

        box_command.pack_start(self.text_command, True, True, 0)
        box_command.pack_end(send_button, False, True, 0)
        info_window.add(self.command_history)

        box_vertical.pack_start(info_window, True, True, 0)
        box_vertical.pack_end(box_command, False, False, 0)

        info_notebook.pack_end(box_vertical, True, True, 0)

    def send_command(self, button, command):
        text = command()
        self.text_command.set_text('')

        iter = self.command_history_buffer.get_end_iter()
        self.command_history_buffer.insert(iter, text+"\n")

        c = UrbanConnect(self.data.host, self.data.port)
        a = c.send_command(self.data.admin_password, text)

        iter = self.command_history_buffer.get_end_iter()
        for d in a:
            self.command_history_buffer.insert(iter, d+'\n')

    def setup_info(self, notebook):
        info_notebook = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        info_notebook.set_border_width(10)

        notebook.append_page(info_notebook, Gtk.Label('Info'))

        info_window = Gtk.ScrolledWindow()
        info_window.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)

        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        box.set_valign(Gtk.Align.START)
        box.set_halign(Gtk.Align.START)

        name = Gtk.Label()
        name.set_markup('<span size="xx-large">%s</span>' % html.escape(self.data.hostname))
        name.set_valign(Gtk.Align.START)
        name.set_halign(Gtk.Align.START)
        name.set_line_wrap(True)
        box.add(name)

        name = Gtk.Label()
        name.set_markup('<span size="x-large">%s:%s</span>\n' % (self.data.host, self.data.port))
        name.set_valign(Gtk.Align.START)
        name.set_halign(Gtk.Align.START)
        box.add(name)

        name = Gtk.Label()
        name.set_markup('<span size="x-large">Players:\t\t %s/%s</span>' % (len(self.data.playerlist), self.data.max_players))
        name.set_valign(Gtk.Align.START)
        name.set_halign(Gtk.Align.START)
        box.add(name)

        name = Gtk.Label()
        name.set_markup('<span size="x-large">Map:\t\t %s</span>' % self.data.map)
        name.set_valign(Gtk.Align.START)
        name.set_halign(Gtk.Align.START)
        box.add(name)

        name = Gtk.Label()
        name.set_markup('<span size="x-large">Gametype:\t %s</span>' % self.data.gametype)
        name.set_valign(Gtk.Align.START)
        name.set_halign(Gtk.Align.START)
        box.add(name)

        info_window.add(box)

        info_notebook.pack_end(info_window, True, True, 0)

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
            self.players_list.add(ListPlayerData(player, self.win))

        self.players_list.connect('row-activated', lambda widget, row: row.select_player())
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

        favorite_button = Gtk.Button()
        if self.load.is_favorite_server(self.data):
            favorite_button.set_label('Remove favorites')
            favorite_button.connect('clicked', self.delete_server)
        else:
            favorite_button.set_label('Add favorites')
            favorite_button.connect('clicked', self.favorite_server)

        button_box.pack_start(favorite_button, True, True, 0)

        play_button = Gtk.Button()
        play_button.set_label('Play')
        play_button.connect('clicked', self.play_button)

        if not self.settings.get_game_location(self.data.game):
            play_button.set_sensitive(False)

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
        self.backa.show()

    def reload_data(self, button):
        self.load.update_server_data(self.data)
        self.win.remove(self.box_outer)
        self.setup(self.data, self.backa, self.load)

    def delete_server(self, button):
        self.load.delete_server(self.data)
        button.set_label('Add favorites')
        button.connect('clicked', self.favorite_server)

    def favorite_server(self, button):
        print(self.data)
        if not self.load.is_favorite_server(self.data):
            self.load.add_new_server(self.data.host, self.data.port, self.data.game)

            button.set_label('Remove favorites')
            button.connect('clicked', self.delete_server)

    def play_button(self, button):
        location = self.settings.get_game_location(self.data.game)
        if self.data.server_password is None:
            os.system('%s +connect %s:%s &' % (location, self.data.host, self.data.port))
        else:
            os.system('%s +connect %s:%s +password %s &' % (location, self.data.host, self.data.port, self.data.server_password))
