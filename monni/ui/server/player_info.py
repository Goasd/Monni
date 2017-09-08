from gi.repository import Gtk


class PlayerInfo:

    def __init__(self, win):
        self.win = win

        self.pop = Gtk.Window(type=Gtk.WindowType.TOPLEVEL)
        self.pop.set_position(Gtk.WindowPosition.CENTER_ON_PARENT)
        self.pop.set_transient_for(win)
        self.pop.set_size_request(450, 300)
        self.setup_header()
        self.pop.show_all()


    def setup(self, player):
        self.pop.set_title('Player')
        self.box_outer = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        self.box_outer.set_valign(Gtk.Align.START)
        self.box_outer.set_halign(Gtk.Align.START)
        label = Gtk.Label()
        label.set_markup('<span size="x-large">'
                         'Name:\t%s\n'
                         'Score:\t%s\n'
                         'Ping:\t%s\n'
                         '</span>'
                         % (player.name, player.score, player.ping))
        label.set_valign(Gtk.Align.START)
        label.set_halign(Gtk.Align.START)
        self.box_outer.pack_start(label, True, True, 0)
        self.box_outer.show_all()
        self.pop.add(self.box_outer)

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
