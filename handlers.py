# PyGObject imports
import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
# other imports
import asyncio
import websockets
from subprocess import Popen, PIPE

class Handlers:
	def onExitClicked(self, *args):
		Gtk.main_quit()
		
	# handlers for dialogs
	def onAboutClicked(self, *args):
		self.dialog_about.run()
		self.dialog_about.hide()

	def onHelpClicked(self, *args):
		self.dialog_help.run()
		self.dialog_help.hide()

	def onSettingsClicked(self, *args):
		self.dialog_settings.run()
		self.dialog_settings.hide()
	
	# tray icon handlers
	def onScrollEvent_indicator(self, instance, steps, direction):
		if direction.value_nick == "up":
			if int(self.backlight) <= (100 - self.step):
				self.backlight = str(int(self.backlight) + self.step)
				
		elif direction.value_nick == "down":
			if int(self.backlight) >= (0 + self.step):
				self.backlight = str(int(self.backlight) - self.step)
		self.tray.props.icon_name = (str(self.cwd / "icons" / f'{self.backlight}.png'))
		asyncio.run(self.send_backlight(self.backlight))
	
	def onScrollEvent_xapp(self, status_icon, amount, direction, time):
		if direction == 0:
			if int(self.backlight) <= (100 - self.step):
				self.backlight = str(int(self.backlight) + self.step)
	
		elif direction == 1:
			if int(self.backlight) >= (0 + self.step):
				self.backlight = str(int(self.backlight) - self.step)
		self.tray.set_icon_name(str(self.cwd / "icons" / f'{self.backlight}.png'))
		asyncio.run(self.send_backlight(self.backlight))
	
	# helper functions
	def round_value(self, current_value: str, step: int = 5) -> str:
		"""Round the current_value to nearest lower value, according to step."""
		rounded_value = current_value - (current_value%step)
		return rounded_value
	
	def get_current_backlight_value(self):
		ask_ddcutil = Popen(['ddcutil', 'get', '10', '--terse'], stdout=PIPE, stderr=PIPE)
		stdout, stderr = ask_ddcutil.communicate()
		backlight = stdout.decode().split()[3]
		return backlight
		
	
	
	# async helpers
	async def send_backlight(self, value):
		"""Corutine to send backlight value to websocket server (if websocket server recieve value, it will set the value directly over ddcutil)"""
		async with websockets.connect(self.ws_server) as websocket:
			await websocket.send(value)
			#await websocket.recv()
	
	
		