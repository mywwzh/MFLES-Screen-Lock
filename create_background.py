from PIL import Image, ImageDraw, ImageFont

image = Image.open("./background.jpg")
draw = ImageDraw.Draw(image)

# 设置文字的字体、大小、颜色、位置
font = ImageFont.truetype("C:/Windows/Fonts/Msyh.ttc", 40)
color = "white"

# 添加文字到画布
draw.text((1630, 970), "MFLES Screen Lock v1.2.0", font=ImageFont.truetype("C:/Windows/Fonts/Msyh.ttc", 18), fill=color)
draw.text((1660, 1000), "Build 2024-04-21", font=ImageFont.truetype("C:/Windows/Fonts/Msyh.ttc", 18), fill=color)
draw.text((1560, 1030), "Copyright (C) 2024 刘子涵 保留所有权利", font=ImageFont.truetype("C:/Windows/Fonts/Msyh.ttc", 18), fill=color)

draw.text((880, 635), "扫码解锁", font=font, fill=color)
# 保存修改后的图片
image.save("./background_with_text.jpg")
