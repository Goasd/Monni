from gi.repository import Gtk


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
        button.connect('clicked', self.add_host_and_port, 'Urban Terror')
        button.set_size_request(10, 10)
        self.box_outer.pack_start(button, True, True, 0)

        button = Gtk.Button()
        button.set_label('Teeworlds')
        button.connect('clicked', self.add_host_and_port, 'Teeworlds')
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
        print(hostname)
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