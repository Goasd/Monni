import os
import threading

import gi

from ..games.loading import Load, servers, l

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gio


class Settings:

    def __init__(self, win, load):
        self.load = load
        self.win = win

        self.pop = Gtk.Window(type=Gtk.WindowType.TOPLEVEL)
        self.pop.set_position(Gtk.WindowPosition.CENTER_ON_PARENT)
        self.pop.set_transient_for(win)
        self.pop.set_size_request(450, 300)
        self.setup_header()
        self.pop.show_all()

        self.select_game()

    def on_tree_selection_changed(self, selection):
        model, treeiter = selection.get_selected()
        if treeiter != None:
            self.game_settings(model[treeiter][0])

    def select_game(self):
        self.pop.set_title('Settings - Monni')
        self.box_outer = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        store = Gtk.ListStore(str)
        store.append(["Urban Terror"])

        tree = Gtk.TreeView(store)
        renderer = Gtk.CellRendererText()
        column = Gtk.TreeViewColumn("Game", renderer, text=0)
        tree.append_column(column)

        select = tree.get_selection()
        select.connect("changed", self.on_tree_selection_changed)

        self.box_outer.pack_start(tree, True, True, 0)
        self.box_outer.show_all()
        self.pop.add(self.box_outer)

    def game_settings(self, game):
        settings_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)

        button1 = Gtk.Button("Choose game ")
        button1.connect("clicked", self.on_file_clicked, game)
        settings_box.add(button1)

        self.box_outer.pack_start(settings_box, True, True, 0)
        self.box_outer.show_all()

    def on_file_clicked(self, widget, game):
        dialog = Gtk.FileChooserDialog("Please choose a file", self.pop,
            Gtk.FileChooserAction.OPEN,
            (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
             Gtk.STOCK_OPEN, Gtk.ResponseType.OK))

        response = dialog.run()

        if response == Gtk.ResponseType.OK:
            self.load.settings_set_game_location(game, dialog.get_filename())

        dialog.destroy()


    def setup_header(self):
        header = Gtk.HeaderBar()
        header.set_show_close_button(False)

        button = Gtk.Button()
        button.set_relief(Gtk.ReliefStyle.NONE)
        img = Gtk.Image.new_from_icon_name("window-close-symbolic", Gtk.IconSize.MENU)
        button.set_image(img)
        button.connect("clicked", self.quit)

        header.pack_end(button)
        self.pop.set_titlebar(header)

    def quit(self, button):
        self.pop.destroy()


class NewServer:

    def __init__(self, win, load):
        self.load = load
        self.win = win

        self.pop = Gtk.Window(type=Gtk.WindowType.TOPLEVEL)
        self.pop.set_position(Gtk.WindowPosition.CENTER_ON_PARENT)
        self.pop.set_transient_for(win)
        self.pop.set_size_request(450,300)
        self.setup_header()
        self.pop.show_all()
        self.pop.set_modal(True)

        self.select_game()

    def select_game(self):
        self.pop.set_title('Add server: Select game')
        self.box_outer = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)

        button = Gtk.Button()
        button.set_label('Urban terror')
        button.connect('clicked', self.add_host_and_port, 'urbanterror')
        button.set_size_request(10, 10)
        self.box_outer.pack_start(button, True, True, 0)

        self.box_outer.show_all()
        self.pop.add(self.box_outer)

    def add_host_and_port(self, button, game):
        self.pop.remove(self.box_outer)
        self.pop.set_title('Add server: Hostname and port')

        self.box_outer = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)

        self.hostname = Gtk.Entry()
        self.hostname.set_text("Hostname")
        self.box_outer.pack_start(self.hostname, True, True, 0)

        self.port = Gtk.Entry()
        self.port.set_text("Port")
        self.box_outer.pack_start(self.port, True, True, 0)

        button = Gtk.Button()
        button.set_label('Save')
        button.connect('clicked', self.save_server, self.hostname.get_text, self.port.get_text, game)
        button.set_size_request(10, 10)
        self.box_outer.pack_start(button, True, True, 0)

        self.box_outer.show_all()
        self.pop.add(self.box_outer)

    def save_server(self, button, hostname, port, game):
        self.load.add_new_server(hostname(), int(port()), game)
        self.pop.destroy()

    def setup_header(self):
        header = Gtk.HeaderBar()
        header.set_show_close_button(False)

        button = Gtk.Button()
        button.set_relief(Gtk.ReliefStyle.NONE)
        img = Gtk.Image.new_from_icon_name("window-close-symbolic", Gtk.IconSize.MENU)
        button.set_image(img)
        button.connect("clicked", self.quit)

        header.pack_end(button)
        self.pop.set_titlebar(header)

    def quit(self, button):
        self.pop.destroy()


class ListPlayerData(Gtk.ListBoxRow):

    def __init__(self, score, ping, player):
        super(Gtk.ListBoxRow, self).__init__()
        self.score = score
        self.ping = ping
        self.player = player
        self.setup_row()

    def setup_row(self):
        row = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        row.set_hexpand(False)
        row.set_vexpand(False)
        data_label = Gtk.Label()
        data_label.set_text(self.score)
        data_label.set_width_chars(5)
        data_label.set_valign(Gtk.Align.START)
        data_label.set_halign(Gtk.Align.START)
        data_label.set_justify(Gtk.Justification.LEFT)

        row.pack_start(data_label, True, True, 0)
        data_label = Gtk.Label()
        data_label.set_text(self.ping)
        data_label.set_width_chars(5)
        data_label.set_valign(Gtk.Align.START)
        data_label.set_halign(Gtk.Align.CENTER)
        data_label.set_justify(Gtk.Justification.LEFT)

        row.pack_start(data_label, True, True, 0)
        data_label = Gtk.Label()
        data_label.set_text(self.player)
        data_label.set_width_chars(20)
        data_label.set_valign(Gtk.Align.START)
        data_label.set_halign(Gtk.Align.END)
        data_label.set_justify(Gtk.Justification.LEFT)

        row.pack_start(data_label, True, True, 0)
        self.add(row)

    def select_player(self):
        print(self.player)


class ServerPage:

    def __init__(self, win, load, home):
        self.win = win
        self.data = None
        self.load = load
        self.home = home

    def setup_serverpage(self, data):
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
        players = self.data.get_players()

        for player in players:
            self.players_list.add(ListPlayerData(player[0], player[1], str(player[2])))

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
        configs = self.data.server_configs()
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
        reload_button.set_size_request(-1, -1)

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
            return int(row_1.score) < int(row_2.score)

        self.players_list.set_sort_func(sort_func, None, False)

    def order_by_ping(self, button, b):

        def sort_func(row_1, row_2, data, notify_destroy):
            return int(row_1.ping) > int(row_2.ping)

        self.players_list.set_sort_func(sort_func, None, False)

    def order_by_name(self, button, b):

        def sort_func(row_1, row_2, data, notify_destroy):
            return row_1.player > row_2.player

        self.players_list.set_sort_func(sort_func, None, False)

    def back(self, button):
        self.win.remove(self.box_outer)
        self.home.show_home()

    def reload_data(self, button):
        self.data.update_data()
        self.win.remove(self.box_outer)
        self.setup_serverpage(self.data)

    def delete_server(self, button):
        self.load.delete_server(self.data)
        self.back(None)

    def play_button(self, button):
        location = self.load.settings_get_game_location(self.data.game)
        os.system('%s +set net_ip %s +set net_port %s' % (location, self.data.host, self.data.port))


class ListServerData(Gtk.ListBoxRow):

    def __init__(self, data, win, load, home, page):
        super(Gtk.ListBoxRow, self).__init__()
        self.data = data
        self.win = win
        self.load = load
        self.home = home
        self.page = page

        self.a = Gtk.Label(data.hostname)
        self.a.set_padding(10,10)
        self.a.set_line_wrap(True)
        self.a.set_valign(Gtk.Align.START)
        self.a.set_halign(Gtk.Align.START)
        self.a.set_justify(Gtk.Justification.LEFT)

        self.b = Gtk.Label(data.hostname)
        self.b.set_padding(10, 10)
        self.b.set_line_wrap(True)
        self.b.set_valign(Gtk.Align.START)
        self.b.set_halign(Gtk.Align.END)
        self.b.set_justify(Gtk.Justification.RIGHT)

        box_outer = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        box_outer.pack_start(self.a, True, True, 0)
        box_outer.pack_end(self.b, True, True, 0)

        self.add(box_outer)

        thread = threading.Thread(target=self.update, args=())
        thread.daemon = True
        thread.start()

    def select_server(self):
        self.win.remove(self.home.stack_box)
        self.page.setup_serverpage(self.data)

    def update(self):
        self.a.set_markup('<span size="x-large">%s</span>\n<span>%s:%s</span>' %
                          (
                              self.data.hostname,
                              self.data.host,
                              self.data.port
                          )
                          )
        self.b.set_markup('<span size="large">Players %s/%s</span>\n<span>%s</span>' %
                          (
                              self.data.get_players_online(),
                              self.data.get_players_max(),
                              self.data.mapname
                          )
                          )


class Home:
    def __init__(self, win, load):
        self.load = load
        self.win = win

        self.servers = Gtk.ListBox()
        self.servers.set_hexpand(True)
        self.servers.set_vexpand(True)
        self.servers.set_border_width(30)

        self.page = ServerPage(self.win, self.load, self)
        self.stack_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)

    def show_home(self):
        self.win.add(self.stack_box)
        self.set_title()

    def setup_home(self):

        self.setup_header()

        stack = Gtk.Stack()
        stack.set_transition_type(Gtk.StackTransitionType.SLIDE_LEFT_RIGHT)

        self.setup_favorites(stack)

        self.setup_server_lists(stack)

        stack_switcher = Gtk.StackSwitcher()
        stack_switcher.set_stack(stack)
        stack_switcher.set_valign(Gtk.Align.START)
        stack_switcher.set_halign(Gtk.Align.CENTER)

        self.stack_box.pack_start(stack_switcher, False, True, 0)
        self.stack_box.pack_end(stack, True, True, 0)

        self.win.add(self.stack_box)
        self.win.show_all()

    def setup_server_lists(self, stack):
        label = Gtk.Label()
        stack.add_titled(label, "label", "Server lists")

    def setup_favorites(self, stack):
        favorites_grid = Gtk.Grid()
        favorites_grid.set_hexpand(True)
        favorites_grid.set_vexpand(True)

        search = self.setup_search()
        favorites_grid.attach(search, 0, 2, 1, 1)

        servers_window = Gtk.ScrolledWindow()
        servers_window.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        servers_window.set_hexpand(True)
        servers_window.set_vexpand(True)

        servers_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        server_list = self.setup_serverlist()
        servers_box.pack_start(server_list, True, True, 0)
        servers_window.add(servers_box)
        favorites_grid.attach(servers_window, 0, 3, 1, 1)

        favorites_down = self.setup_favorites_down()
        favorites_grid.attach(favorites_down, 0, 4, 1, 1)

        stack.add_titled(favorites_grid, "grid", "Favorites")

    def setup_favorites_down(self):
        favorites_down = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)

        new_server_button = Gtk.Button()
        new_server_button.set_relief(Gtk.ReliefStyle.NONE)
        new_server_button.set_label('New server')
        new_server_button.connect("clicked", self.new_server)
        favorites_down.pack_start(new_server_button, True, True, 0)

        update_servers_button = Gtk.Button()
        update_servers_button.set_relief(Gtk.ReliefStyle.NONE)
        update_servers_button.set_label('Update servers')
        update_servers_button.connect("clicked", self.update_servers)
        favorites_down.pack_end(update_servers_button, True, True, 0)

        return favorites_down

    def setup_header(self):
        header = Gtk.HeaderBar()
        header.set_show_close_button(False)

        button = Gtk.Button()
        button.set_relief(Gtk.ReliefStyle.NONE)
        img = Gtk.Image.new_from_icon_name("emblem-system-symbolic", Gtk.IconSize.MENU)
        button.set_image(img)
        button.connect("clicked", self.settings)

        header.pack_start(button)

        button = Gtk.Button()
        button.set_relief(Gtk.ReliefStyle.NONE)
        img = Gtk.Image.new_from_icon_name("window-close-symbolic", Gtk.IconSize.MENU)
        button.set_image(img)
        button.connect("clicked", self.quit)

        header.pack_end(button)
        seperator = Gtk.Separator.new(Gtk.Orientation.VERTICAL)
        header.pack_end(seperator)
        self.win.set_titlebar(header)
        self.set_title()

    def set_title(self):
        self.win.set_title("Monni")

    def settings(self, button):
        Settings(self.win, self.load)

    def quit(self, button):
        self.win.destroy()

    def setup_search(self):
        searchbar = Gtk.SearchBar()
        searchentry = Gtk.SearchEntry()
        searchentry.set_size_request(500,-1)
        searchentry.set_hexpand(True)
        searchbar.set_hexpand(True)

        searchentry.connect("search-changed", self.on_search_changed)
        searchbar.connect_entry(searchentry)
        searchbar.add(searchentry)
        searchbar.set_search_mode(True)

        searchbar.set_valign(Gtk.Align.CENTER)
        searchbar.set_halign(Gtk.Align.CENTER)
        return searchbar

    def on_search_changed(self, searchentry):
        data = searchentry.get_text()

        def filter_func(row, data, notify_destroy):
            if data is '':
                return True
            if row.data.hostname is None:
                return False
            if data in row.data.hostname.lower():
                return True
            if data in row.data.host.lower():
                return True
            if data in row.data.mapname.lower():
                return True
            return False

        self.servers.set_filter_func(filter_func, data, False)

    def setup_serverlist(self):

        for server in servers:
            self.add_server_in_servers(server)

        def sort_func(row_1, row_2, data, notify_destroy):
            return len(row_1.data.playerlist) < len(row_2.data.playerlist)

        self.servers.set_sort_func(sort_func, None, False)
        self.servers.connect('row-activated', lambda widget, row: row.select_server())
        return self.servers

    def add_server_in_servers(self, server):
        self.servers.add(ListServerData(server, self.win, self.load, self, self.page))
        self.servers.show_all()

    def update_servers(self, button):
        for server in self.servers.get_children():

            thread = threading.Thread(target=self.update_server, args=(server,))
            thread.daemon = True
            thread.start()

    def update_server(self, server):
        server.data.update_data()
        server.update()

        def sort_func(row_1, row_2, data, notify_destroy):
            return len(row_1.data.playerlist) < len(row_2.data.playerlist)

        l.acquire()
        self.servers.set_sort_func(sort_func, None, False)
        l.release()

    def new_server(self, button):
        NewServer(self.win, self.load)

    def server_created(self, server):
        self.add_server_in_servers(server)

    def server_deleted(self, delete_server):
        for server in self.servers:
            if server.data == delete_server:
                self.servers.remove(server)


class Window(Gtk.ApplicationWindow):

    def __init__(self, app):
        Gtk.Window.__init__(self, application=app)
        load = Load()

        self.set_position(Gtk.WindowPosition.CENTER)
        self.set_size_request(500, 500)
        self.home = Home(self, load)
        self.home.setup_home()

        load.call_when_server_created = self.home.server_created
        load.call_when_server_deleted = self.home.server_deleted
        load.servers()


class Application(Gtk.Application):
    def __init__(self):

        Gtk.Application.__init__(self, application_id="apps.monni",
                                 flags=Gio.ApplicationFlags.FLAGS_NONE)

    def do_startup(self):
        Gtk.Application.do_startup(self)

    def do_activate(self):
        win = Window(self)
        win.show_all()

