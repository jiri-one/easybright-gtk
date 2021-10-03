from PIL import Image, ImageDraw, ImageFont
#img = Image.new(mode, size, color)
#img.save(filename)

font = ImageFont.truetype("/usr/share/fonts/liberation/LiberationSans-Regular.ttf", 90)

img = Image.new("RGB", (100, 100), "white")
img.putalpha(0)
d = ImageDraw.Draw(img)
d.text((0,0), "50", font=font, fill='red')
img.save('tray.png')