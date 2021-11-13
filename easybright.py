import gi
gi.require_version("XApp", "1.0")
gi.require_version('AyatanaAppIndicator3', '0.1')
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
from gi.repository import AyatanaAppIndicator3 as AppIndicator
from subprocess import Popen, PIPE
import asyncio
import websockets
from time import sleep
from PIL import Image, ImageDraw, ImageFont

from pathlib import Path
cwd = Path(__file__).parent

#Popen(["python", str(cwd / "async_tests" / "websocket_server.py")])
ask_ddcutil = Popen(
	['ddcutil', 'get', '10', '--terse'],
	stdout=PIPE,
	stderr=PIPE)
stdout, stderr = ask_ddcutil.communicate()
backlight = stdout.decode().split()[3]

async def send_backlight(value):
	async with websockets.connect("ws://localhost:8888") as websocket:
		await websocket.send(value)
		#await websocket.recv()


class EasyBright():
	def __init__(self):
		#self.window = Gtk.Window()
		#self.window.show()
		#self.window.connect("destroy", Gtk.main_quit)
		self.backlight = backlight
		self.tray = AppIndicator.Indicator.new(id="111",icon_name=str(cwd / "icons" / f'{self.backlight}.png'), category=1)
		print(self.tray.get_category())
		print(self.tray.get_id())
		self.tray.set_status(AppIndicator.IndicatorStatus.ACTIVE)
		#self.tray.props.icon_name = str(cwd / "icons" / f'{self.backlight}.png')
		self.step = 5
		#self.tray.set_label(self.backlight)
		#self.tray.set_tooltip_text("EasyBright - The best way to set backlight of your screen")
		self.tray.connect("scroll-event", self.onScrollEvent)
		self.menu_setup()
		self.tray.set_menu(self.menu)

	def menu_setup(self):
		self.menu = Gtk.Menu()
		self.to_bs_menu = Gtk.MenuItem(label="ई.सं. बाट बि.सं.")
		self.to_ad_menu = Gtk.MenuItem(label="बि.सं. बाट ई.सं.")
		self.to_ad_menu.show()
		self.to_bs_menu.show()
		self.quit_item = Gtk.MenuItem(label="बन्द")
		self.quit_item.show()
	
	def onScrollEvent(self, instance, steps, direction):
		if direction.value_nick == "up":
			if int(self.backlight) <= (100 - self.step):
				self.backlight = str(int(self.backlight) + self.step)
				
		elif direction.value_nick == "down":
			if int(self.backlight) >= (0 + self.step):
				self.backlight = str(int(self.backlight) - self.step)
				
			#print(self.backlight)
			#self.tray.set_label(str(self.backlight))
			#self.create_png_text_icon(self.backlight)
		self.tray.props.icon_name = (str(cwd / "icons" / f'{self.backlight}.png'))
		asyncio.run(send_backlight(self.backlight))	
	
	def send_backlight_to_websocket_server(self):
		while True:
			sleep(1)
			asyncio.run(send_backlight(self.backlight))	
	
	def create_png_text_icon(self, backlight):
		font = ImageFont.truetype("/usr/share/fonts/liberation/LiberationSans-Regular.ttf", 90)
		img = Image.new("RGB", (100, 100), "white")
		img.putalpha(0)
		d = ImageDraw.Draw(img)
		d.text((0,0), backlight, font=font, fill='red')
		img.save('tray.png')
		
if __name__ == '__main__':
	gui = EasyBright()
	Gtk.main()
