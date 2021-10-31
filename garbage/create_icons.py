from PIL import Image, ImageDraw, ImageFont
#img = Image.new(mode, size, color)
#img.save(filename)

# icon for 0 and 5
font = ImageFont.truetype("/usr/share/fonts/liberation/LiberationSans-Regular.ttf", 90)
img = Image.new("RGB", (100, 100), "white")
img.putalpha(0)
d = ImageDraw.Draw(img)	
d.text((25,0), "0", font=font, fill='red')
img.save('../icons/0.png')

img = Image.new("RGB", (100, 100), "white")
img.putalpha(0)
d = ImageDraw.Draw(img)	
d.text((25,0), "5", font=font, fill='red')
img.save('../icons/5.png')

# icons from 10 to 95
for backlight in range(10,100,5):
	img = Image.new("RGB", (100, 100), "white")
	img.putalpha(0)
	d = ImageDraw.Draw(img)	
	d.text((0,0), f"{backlight}", font=font, fill='red')
	img.save(f'../icons/{str(backlight)}.png')

# icon for 100
font = ImageFont.truetype("/usr/share/fonts/liberation/LiberationSans-Regular.ttf", 60)
img = Image.new("RGB", (100, 100), "white")
img.putalpha(0)
d = ImageDraw.Draw(img)	
d.text((0,15), "100", font=font, fill='red')
img.save('../icons/100.png')