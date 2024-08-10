import time
import numpy as np
from pywinauto import Application
import win32gui
import win32con
from PIL import Image

class Window:
    def __init__(self, hwnd,hwnd_bind):
        self.hwnd = int(hwnd)
        self.app = Application().connect(handle=self.hwnd)
        self.dlg = self.app.window(handle=self.hwnd) 
        
        self.hwnd_bind = int(hwnd_bind)
        self.app_bind = Application().connect(handle=self.hwnd_bind)
        self.dlg_bind = self.app.window(handle=self.hwnd_bind)      
    
    def bring_to_front(self):
        """将窗口置于前景，防止被遮挡或最小化"""
        if self.dlg.is_minimized():
            self.dlg.restore()  # 恢复最小化的窗口
        win32gui.SetForegroundWindow(self.hwnd)  # 将窗口置于前景


    def capture_screenshot(self, filename=None):
        """捕获窗口截图"""
        self.bring_to_front()
        #time.sleep(0.5)  # 给窗口一些时间来绘制
        image = self.dlg_bind.capture_as_image()
        
        if filename:
            image.save(filename)
            print(f"截图已保存至 {filename}")
            
        return image
    
    def get_size(self):
        rect = self.dlg_bind.rectangle()
        width = rect.width()
        height = rect.height()
        return width, height
    
    def isScreenHorizontal(self):
        width, height = self.get_size()
        #print( width, height)
        if width > height:
            return True
        else:
            return False


def count_pixels_below_threshold(img):
    # 打开图像并转换为灰度
    image = img.convert('L')
    threshold = 128
    # 获取图像的像素值
    pixel_values = list(image.getdata())
    
    # 计算灰度值小于阈值的像素点数量
    below_threshold_count = sum(1 for pixel in pixel_values if pixel < threshold)
    
    return below_threshold_count/len(pixel_values)

def is_color_close(color, target, tolerance=30):
    if abs(int(color[0]) - target[0]) <= tolerance and abs(int(color[1]) - target[1]) <= tolerance and abs(int(color[2]) - target[2]) <= tolerance:
        return True
    else:
        return False

def go(img):

    left = 547 / 585 * img.width
    top = 890 / 1044 * img.height
    right = 561 / 585 * img.width
    bottom = 926 / 1044 * img.height

    # 裁剪图像
    cropped_img = img.crop((left, top, right, bottom))
    cropped_img.save('go.png')

    pixels = np.array(cropped_img)
    total_pixels = pixels.shape[0] * pixels.shape[1]
    target_color = [17, 232, 154]
    tolerance = 10
    close_pixels = sum(is_color_close(pixel, target_color, tolerance) for row in pixels for pixel in row)

    # 计算占比
    percentage = close_pixels / total_pixels
    #print(percentage)
    if percentage > 0.9:
        return True
    else:
        return False
    
def countdown(img):
    left = 3 / 4 * img.width
    top = 0
    right = img.width
    bottom =img.height

    # 裁剪图像
    cropped_img = img.crop((left, top, right, bottom))
    cropped_img.save('go.png')

    pixels = np.array(cropped_img)
    total_pixels = pixels.shape[0] * pixels.shape[1]
    target_color = [34, 192, 130]
    tolerance = 20
    close_pixels = sum(is_color_close(pixel, target_color, tolerance) for row in pixels for pixel in row)

    # 计算占比
    percentage = close_pixels / total_pixels
    #print(percentage)
    if percentage > 0.9:
        return True
    else:
        return False
def calculate_image_mean(image_path):
    # 打开图片
    image = Image.open(image_path)
    # 将图片转换为 numpy 数组
    image_array = np.array(image)
    # 分离 RGB 通道
    red_channel = image_array[:, :, 0]
    green_channel = image_array[:, :, 1]
    blue_channel = image_array[:, :, 2]
    # 计算每个通道的均值
    red_mean = np.mean(red_channel)
    green_mean = np.mean(green_channel)
    blue_mean = np.mean(blue_channel)
    # 返回结果
    return red_mean, green_mean, blue_mean



if __name__ == '__main__':
    window = Window(2097858,1967034)
    print(window.get_size())
    img = window.capture_screenshot('go_.png')
    print(count_pixels_below_threshold(img))
    go(img)
