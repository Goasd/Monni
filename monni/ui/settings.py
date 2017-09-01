from gi.repository import Gtk


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

        setting_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)

        game_name = Gtk.Label()
        game_name.set_markup('<span size="x-large">%s</span>' % game)
        game_name.set_valign(Gtk.Align.START)
        game_name.set_halign(Gtk.Align.START)

        settings_box.add(game_name)

        game_name = Gtk.Label()
        game_name.set_markup('Game location')
        game_name.set_valign(Gtk.Align.CENTER)
        game_name.set_halign(Gtk.Align.CENTER)

        setting_box.add(game_name)


        folder = Gtk.Entry()
        folder.set_text(self.load.settings_get_game_location(game))
        setting_box.add(folder)
        button1 = Gtk.Button("...")
        button1.connect("clicked", self.on_file_clicked, game)
        setting_box.add(button1)

        settings_box.add(setting_box)

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