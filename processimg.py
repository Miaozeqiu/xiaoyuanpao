from PIL import Image

# 打开图像文件
image = Image.open('moniqi/YDXYSJ.png')

# 定义裁剪框的坐标：(left, upper, right, lower)
# 这里指定裁剪框的具体位置和尺寸
left = 0 #1616 - 1656是右侧边栏的位置
top = 0
right = 64
bottom = 64

# 使用crop方法进行裁剪
cropped_image = image.crop((left, top, right, bottom))
cropped_image = cropped_image.convert('RGB')
# 显示裁剪后的图像
cropped_image.show()

# 保存裁剪后的图像
cropped_image.save('moniqi/YDXYSJ_.jpg')