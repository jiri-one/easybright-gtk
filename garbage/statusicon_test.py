#!/usr/bin/python3

import gi
gi.require_version('XApp', '1.0')
from gi.repository import XApp, Gtk, Gdk
from gi.repository import GLib, GObject
import sys

"""
This variant tests behavior of giving a only a secondary menu to the StatusIcon instance.
This results in 'activate' signals being sent for primary clicks only.
"""

class App(GObject.Object):

    def __init__(self):
        super(App, self).__init__()
        self.status_icon = XApp.StatusIcon()
        self.status_icon.connect("state-changed", self.on_icon_state_changed)

        self.status_icon.set_icon_name("folder-symbolic")
        self.status_icon.set_tooltip_text("Testing primary activate and secondary menu")
        self.status_icon.set_label("label 1")
        self.status_icon.set_visible(True)
        self.status_icon.connect("scroll-event", self.handle_scroll_event)

        self.label = None
        self.window = None

        self.counter = 1

        menu = Gtk.Menu()
        menu.append(Gtk.MenuItem.new_with_label("Hi, secondary menu here!"))
        menu.append(Gtk.SeparatorMenuItem())
        menu.append(Gtk.MenuItem.new_with_label("Help me!"))
        menu.show_all()

        self.status_icon.set_secondary_menu(menu)
        self.status_icon.connect("activate", self.on_status_icon_activate)

        GLib.timeout_add_seconds(2, self.on_timeout_cb)

    def on_icon_state_changed(self, icon, new_state):
        print("Icon state changed - the state is now: %s" % new_state)

    def on_timeout_cb(self):
        self.counter += 1
        self.status_icon.set_label("label %d" % self.counter)
        return True

    def on_status_icon_activate(self, icon, button, time):
        print("Activated via button %d" % button)
        self.counter = 0
        self.status_icon.set_label("label %d" % self.counter)
        self.make_window()

    def make_window(self):
        w = Gtk.Window(default_width=300, default_height=130)
        b = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        w.add(b)
        self.label = Gtk.Label("How can I help you?")
        b.pack_start(self.label, True, True, 0)

        self.window = w
        w.show_all()

    def handle_scroll_event(self, icon, amount, orientation, time, data=None):
        if self.window == None:
            self.make_window()

        if orientation == XApp.ScrollDirection.UP:
            self.label.set_text("Scrolled Up !")
        elif orientation == XApp.ScrollDirection.DOWN:
            self.label.set_text("Scrolled Down!")
        elif orientation == XApp.ScrollDirection.LEFT:
            self.label.set_text("Scrolled Left!")
        else:
            self.label.set_text("Scrolled Right!")


if __name__ == '__main__':
    GLib.setenv ("G_MESSAGES_DEBUG", "all", True)
    app = App()
    try:
        GLib.MainLoop().run()
    except KeyboardInterrupt:
        pass
    sys.exit(0)