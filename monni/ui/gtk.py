import gi

from monni.ui.server_lists import ServerLists
from .favorites import Favorites
from .settings import Settings
from ..games.loading import Load

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gio

class Home:
    def __init__(self, win):

        self.load = Load()
        self.win = win

        self.stack_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)

    def show_home(self):
        self.win.add(self.stack_box)
        self.set_title()

    def setup(self):

        self.setup_header()

        stack = Gtk.Stack()
        stack.set_transition_type(Gtk.StackTransitionType.SLIDE_LEFT_RIGHT)

        favorites = Favorites(self.win, self, self.load)
        favorites.setup(stack)

        server_lists = ServerLists(self.win, self, self.load)
        server_lists.setup(stack)

        stack_switcher = Gtk.StackSwitcher()
        stack_switcher.set_stack(stack)
        stack_switcher.set_valign(Gtk.Align.START)
        stack_switcher.set_halign(Gtk.Align.CENTER)

        self.stack_box.pack_start(stack_switcher, False, True, 0)
        self.stack_box.pack_end(stack, True, True, 0)

        self.win.add(self.stack_box)
        self.win.show_all()

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


class Window(Gtk.ApplicationWindow):

    def __init__(self, app):
        Gtk.Window.__init__(self, application=app)

        self.set_position(Gtk.WindowPosition.CENTER)
        self.set_size_request(500, 500)
        self.home = Home(self)
        self.home.setup()


class Application(Gtk.Application):
    def __init__(self):

        Gtk.Application.__init__(self, application_id="apps.monni",
                                 flags=Gio.ApplicationFlags.FLAGS_NONE)

    def do_startup(self):
        Gtk.Application.do_startup(self)

    def do_activate(self):
        win = Window(self)
        win.show_all()

