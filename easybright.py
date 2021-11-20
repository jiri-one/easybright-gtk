# basic imports
from os import environ
from sys import modules
# PyGObject imports
import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

# tray icon imports
if environ.get("DESKTOP_SESSION").lower() in ["plasma", "gnome", "gnome-xorg", "gnome-wayland"]:
	try:
		gi.require_version('AyatanaAppIndicator3', '0.1')
		from gi.repository import AyatanaAppIndicator3 as AppIndicator
		if 'gi.repository.AyatanaAppIndicator3' in modules.keys():
			tray = "AppIndicator"
	except (ValueError, ModuleNotFoundError, NameError):
		print("AyatanaAppIndicator3 not found.")
elif environ.get("DESKTOP_SESSION").lower() in ["cinnamon", "xfce", "mate"]:
	try:
		gi.require_version("XApp", "1.0")
		from gi.repository.XApp import StatusIcon
		if 'gi.repository.XApp' in modules.keys():
			tray = "StatusIcon"
	except (ValueError, ModuleNotFoundError, NameError):
		print("XApps not found.")
else:
	tray = None

# imports from my other files with classes and methods
from tray_menu import TrayMenu
from handlers import Handlers
from settings import Settings
from helpers import Helpers

from pathlib import Path
cwd = Path(__file__).parent

from subprocess import Popen, PIPE

Popen(["python", str(cwd / "async_tests" / "websocket_server.py")])
##### NEED TO CHECK IF IT IS RUNNING

# Handlers and Helpers are classes with pure methods and Settings is class with __init__ method too
class EasyBright(Settings, Handlers, Helpers):
	def __init__(self):
		# basic settings
		super().__init__() # super from Settings __init__ method
		
		# Build GUI from Glade file
		self.builder = Gtk.Builder()
		self.builder.add_from_file(str(self.cwd / "ui" / "easybright.glade"))
		
		# get objects and set them
		gui = self.builder.get_object
		self.dialog_about = gui("dialog_about") # about dialog
		self.dialog_help = gui("dialog_help") # help dialog
		self.dialog_settings = gui("dialog_settings") # settings dialog	
		self.dialog_error = gui("dialog_error") # Error dialog (for any exceptions)	
		self.label_error = gui("label_error") # Here we will set label for error_dialog	
		self.bt_close_error_dialog = gui("bt_close_error") # close button on tray dialog
		self.bt_close_error_dialog.connect("clicked", self.onBtCloseError) # it is not possible to connect it in Glade, so it have to be here (maybe bug in Glade)
		
		# initiate rest of settings
		self.initiate_settings()
		self.backlight = self.backlight_check()
		self.icon_path = str(self.cwd / "icons" / f'{self.backlight}.png')				
		
		# tray menu settings
		self.tooltip = "EasyBright - The best way to set backlight of your screen"
		self.menu = TrayMenu() # tray icon menu from class TrayMenu in file tray_menu.py	
		self.menu.item1.connect("activate", self.onSettingsClicked) # connect menu item Settings
		self.menu.item2.connect("activate", self.onHelpClicked) # connect menu item Help
		self.menu.item3.connect("activate", self.onAboutClicked) # connect menu item About
		self.menu.item4.connect("activate", self.onExitClicked) # connect menu item Exit
		# tray specific settings
		if tray == "AppIndicator":
			self.tray = AppIndicator.Indicator.new(id="easybright",icon_name=self.icon_path, category=3)
			self.tray.set_status(AppIndicator.IndicatorStatus.ACTIVE)
			self.tray.connect("scroll-event", self.onScrollEvent_indicator)
			self.tray.set_menu(self.menu)
		elif tray == "StatusIcon":
			self.tray = StatusIcon()
			self.tray.set_icon_name(self.icon_path)
			self.tray.set_tooltip_text(self.tooltip)
			self.tray.connect("scroll-event", self.onScrollEvent_xapp)
			self.tray.set_secondary_menu(self.menu)
		else: # tray = None
			self.showErrorDialog("""EasyBright-GTK doesn't find any of tray icon supported handler (AyatanaAppIndicator3 or XApp.StatusIcon). If you would run this app, you need to install one of mentioned tray implementation.""")
	
if __name__ == '__main__':
	gui = EasyBright()
	Gtk.main()
