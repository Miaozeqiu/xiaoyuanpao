from pywinauto import Application
import os
import cv2
import numpy as np
from pywinauto.keyboard import send_keys
import pygetwindow as gw
import pyautogui
import time
from PIL import Image
from IsCentralSymmetry import Dispersion



#点击运动校园世界
app = Application().connect(title="雷电模拟器-3")
dlg = app.window(title="雷电模拟器-3")

dlg.set_focus()
#send_keys('{VK_F9}')  #震动
def printscreen():
    screenshot = dlg.capture_as_image()
    screenshot_path = os.path.join(os.getcwd(), "cache.png")
    screenshot.save(screenshot_path)
    return screenshot_path

def crop_image(input_image, output_image,location):
    """
    使用PIL库裁剪图片

    参数:
    input_image (str): 输入图片的文件路径
    output_image (str): 输出图片的文件路径
    left (int): 左边界的像素坐标
    top (int): 上边界的像素坐标
    right (int): 右边界的像素坐标
    bottom (int): 下边界的像素坐标
    """
    left, top, right, bottom = location
    image = Image.open(input_image)
    cropped = image.crop((left, top, right, bottom))
    cropped.save(output_image)


def recognize_elements(image_path, template_path, threshold=0.8,click = False):
    # 读取截图
    img = cv2.imread(image_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # 读取模板
    template = cv2.imread(template_path, cv2.IMREAD_COLOR)
    h, w = template.shape[:2]
    template_gray = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)

    # 模板匹配
    res = cv2.matchTemplate(gray, template_gray, cv2.TM_CCOEFF_NORMED)
    loc = np.where(res >= threshold)
    flag = False
    for pt in zip(*loc[::-1]):
        # 绘制识别到的矩形
        cv2.rectangle(img, pt, (pt[0] + w, pt[1] + h), (0, 255, 0), 2)
        if not flag:
        # 点击识别到的元素
            if click:
                dlg.click_input(coords=(int(pt[0] + w / 2), int(pt[1] + h / 2)))
            flag = True
        

    result_path = os.path.join(os.getcwd(), "result.png")
    cv2.imwrite(result_path, img)
    print(f"识别结果已保存至 {result_path}")



# process = []

# 进行元素识别和点击
screenshot_path = printscreen()
# 模板图片路径（假设你有一个按钮模板）
template_path = os.path.join(os.getcwd(), "moniqi", "YDXYSJ_.jpg")
recognize_elements(screenshot_path, template_path,click = True)

#开屏广告
#检测广告
def jiance(screenshot_path):
    img = cv2.imread(screenshot_path)

    # 转换为灰度图像
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # 定义灰度阈值
    threshold = 100

    # 创建灰度小于阈值的掩码
    mask = cv2.threshold(gray, threshold, 255, cv2.THRESH_BINARY)[1]

    # 计算灰度小于阈值的像素数量
    below_threshold_pixels = cv2.countNonZero(mask)

    # 计算图像总像素数
    total_pixels = img.shape[0] * img.shape[1]

    # 计算灰度小于阈值的像素占比
    below_threshold_ratio = below_threshold_pixels / total_pixels
    if below_threshold_ratio < 0.6:
        print("有广告")
        CloseAd(screenshot_path)
    
    pass


def CloseAd(screenshot_path):
    locations = [[15,65,60, 110],[90,280,115,305]]  #[90,280,115,305]
    for location in locations:
        crop_image(screenshot_path,'cache_croped.png',location)
        std_distance = Dispersion('cache_croped.png','cache_TwoColor.png')
        if std_distance < 0.09:
            dlg.click_input(coords=(int((location[0]+location[2])/2),int((location[1]+location[3])/2)))

         
while True:
    time.sleep(0.1)
    screenshot_path = printscreen()
    if(jiance(screenshot_path)):
        print("弹出广告")