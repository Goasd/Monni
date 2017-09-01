from gi.repository import Gtk


class ServerLists:

    def __init__(self, win, home, load):
        self.win = win
        self.home = home
        self.load = load

    def setup(self, stack):
        label = Gtk.Label()
        stack.add_titled(label, "label", "Server lists")