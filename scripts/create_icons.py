from PIL import Image, ImageDraw, ImageFont
#img = Image.new(mode, size, color)
#img.save(filename)

for backlight in range(1,101):
	img = Image.new("RGB", (100, 100), "white")
	img.putalpha(0)
	font = ImageFont.truetype("/usr/share/fonts/liberation/LiberationSans-Regular.ttf", 90)	
	d = ImageDraw.Draw(img)
	if backlight < 10:
		d.text((25,0), str(backlight), font=font, fill='red')		
	elif backlight >= 10 and backlight < 100:
		d.text((0,0), str(backlight), font=font, fill='red')
	elif backlight == 100:
		font = ImageFont.truetype("/usr/share/fonts/liberation/LiberationSans-Regular.ttf", 60)
		d.text((0,15), str(backlight), font=font, fill='red')
	img.save(f'../icons/{str(backlight)}.png')
