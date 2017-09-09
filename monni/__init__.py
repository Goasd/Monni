import os
import sys

import gi
gi.require_version('Gtk', '3.0')

PACKAGE_PARENT = '..'
SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))

from monni.ui.gtk import Application

if __name__ == "__main__":
    app = Application()
    app.run(None)
