from pywinauto import Application
import os
import cv2
import numpy as np
from pywinauto.keyboard import send_keys
import pygetwindow as gw
import pyautogui
import time



# 关闭应用程序
app = Application().connect(title="雷电模拟器-3")
dlg = app.window(title="雷电模拟器-3")

dlg.set_focus()
#send_keys('{VK_F9}')  #震动
def printscreen():
    screenshot = dlg.capture_as_image()
    screenshot_path = os.path.join(os.getcwd(), "cache.png")
    screenshot.save(screenshot_path)
    return screenshot_path


def recognize_elements(image_path, template_path, threshold=0.8,click = False):
    # 读取截图
    img = cv2.imread(image_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # 读取模板
    template = cv2.imread(template_path, 0)
    w, h = template.shape[::-1]

    # 模板匹配
    res = cv2.matchTemplate(gray, template, cv2.TM_CCOEFF_NORMED)
    loc = np.where(res >= threshold)
    flag = False
    for pt in zip(*loc[::-1]):
        # 绘制识别到的矩形
        cv2.rectangle(img, pt, (pt[0] + w, pt[1] + h), (0, 255, 0), 2)
        if not flag:
        # 点击识别到的元素
            process.append((int(pt[0] + w / 2), int(pt[1] + h / 2)))
            if click:
                dlg.click_input(coords=(int(pt[0] + w / 2), int(pt[1] + h / 2)))
            flag = True
        

    result_path = os.path.join(os.getcwd(), "result.png")
    cv2.imwrite(result_path, img)
    print(f"识别结果已保存至 {result_path}")



process = []

# 进行元素识别和点击
screenshot_path = printscreen()
# 模板图片路径（假设你有一个按钮模板）
template_path = os.path.join(os.getcwd(), "moniqi", "manu.jpg")
recognize_elements(screenshot_path, template_path,click = True)

screenshot_path = printscreen()
template_path = os.path.join(os.getcwd(), "moniqi", "Settings.jpg")
recognize_elements(screenshot_path, template_path,click = False)



window = gw.getWindowsWithTitle('雷电模拟器-3')[0]

# 获取窗口的左上角坐标
window_left, window_top = window.left, window.top

# 假设 process 是一个包含相对于窗口左上角的两个坐标的列表 [(x1, y1), (x2, y2)]


# 点击第一个坐标



# 移动到第二个坐标并点击
pyautogui.moveTo(window_left + process[1][0], window_top + process[1][1])
pyautogui.click()
