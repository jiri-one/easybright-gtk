from pystray import Icon as icon, Menu as menu, MenuItem as item
from PIL import Image, ImageDraw, ImageFont

def create_image():
    # Generate an image and draw a pattern
    font = ImageFont.truetype("/usr/share/fonts/liberation/LiberationSans-Regular.ttf", 90)
    img = Image.new("RGB", (100, 100), "white")
    img.putalpha(0)
    d = ImageDraw.Draw(img)
    d.text((0,0), "50", font=font, fill='red')

    return img

from kivy.clock import Clock
from kivy.app import App
from kivy.config import Config
from kivy.uix.textinput import TextInput
from threading import Thread

Config.set('graphics', 'window_state', 'hidden')
Config.set('graphics', 'borderless', '0')
Config.set('kivy', 'exit_on_escape', '0')

class MyDebugApp(App):
    visible = False
    def build(self):
        return TextInput()
    
    def on_start(self):
        self.root.focus = True    

    def alternate(self):
        if self.visible:
            self.root.get_root_window().hide()
        else:
            self.root.get_root_window().show()

        self.visible = not self.visible

ma = MyDebugApp()       
kivy_app = Thread(target=ma.run)
kivy_app.start()

my_menu = menu(item(text="Show Main Window", action=ma.alternate, default = True))
icon = icon('EasyBright', create_image(), menu=my_menu)
icon.run()

#ICON REFRESH přes icon.icon = image kdykoliv, takže paráda