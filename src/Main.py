#!/usr/bin/env python3

import sys
import json
import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gio, GLib, Gtk

from MainWindow import MainWindow
from util import ComputerManager


def setup_gdk_log_handler():
    def log_handler(domain, level, message, user_data):
        if message and "gdk_x11_window_get_xid" in message:
            return
        GLib.log_default_handler(domain, level, message, user_data)

    GLib.log_set_handler(
        "Gdk",
        GLib.LogLevelFlags.LEVEL_CRITICAL | GLib.LogLevelFlags.LEVEL_WARNING,
        log_handler,
        None,
    )


setup_gdk_log_handler()

if "--json" in sys.argv or "-j" in sys.argv:
    manager = ComputerManager.ComputerManager()
    print(json.dumps(manager.get_all_device_info(), indent=2))
    sys.exit(0)

class Application(Gtk.Application):
    def __init__(self, *args, **kwargs):
        super().__init__(
            *args,
            application_id="org.parslinux.about",
            flags=Gio.ApplicationFlags(8),
            **kwargs,
        )

        self.window = None
        GLib.set_prgname("org.parslinux.about")

        self.setup_options()

    def setup_options(self):
        # Open details page directly
        self.add_main_option(
            "hardware",
            ord("h"),
            GLib.OptionFlags(0),
            GLib.OptionArg(0),
            "Show Hardware Information",
            None,
        )

        # Print only json, don't run gui
        self.add_main_option(
            "json",
            ord("j"),
            GLib.OptionFlags(0),
            GLib.OptionArg(0),
            "Print json report only without GUI",
            None,
        )

    def do_activate(self):
        settings = Gtk.Settings.get_default()

        # prevent label shows selected on startup
        settings.set_property("gtk_label_select_on_focus", False)

        # We only allow a single window and raise any existing ones
        if not self.window:
            # Windows are associated with the application
            # when the last one is closed the application shuts down
            self.window = MainWindow(self)
        else:
            self.window.control_args()

        self.window.ui_main_window.present()

    def do_command_line(self, command_line):
        options = command_line.get_options_dict()
        options = options.end().unpack()
        self.args = options

        self.activate()
        return 0


app = Application()
app.run(sys.argv)
