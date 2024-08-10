import json
import subprocess
import os
import re

import cv2
import numpy as np
from ldconsolefunc import list2
from ldconsolefunc import get_window_size
import time
from pywinauto import Application
root_path = 'C:\leidian\LDPlayer9'
# s= input('请输入姓名：')
# account = input('请输入账户：')
# password = input('请输入密码：')
bindhwnd = '3148486'
n = 7
app = Application().connect(handle=1182374)
dlg = app.window(handle=1182374)  # 获取具有该句柄的窗口

dlg.set_focus()
def printscreen():
    screenshot = dlg.capture_as_image()
    screenshot_path = os.path.join(os.getcwd(), "cache.png")
    screenshot.save(screenshot_path)
    return screenshot_path

def click(hwnd,wh_r):
    w = 720
    h = 1280
    print(w,h)
    w*=wh_r[0]
    h *= wh_r[1]
    print(w,h)
    click_command = ['ld', '-s', '7', 'input', 'tap', str(int(w)),str(int(h))]
    click_process = subprocess.Popen(click_command, cwd=root_path, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    click_process.communicate()
def findEdge(input_path):
    '''
    输入：手机屏幕截图路径
    返回：关闭广告按钮的位置
    '''


    # 读取彩色图像
    img = cv2.imread(input_path)  # 默认以BGR格式读取

    # 获取图像高度和宽度
    height, width, channels = img.shape


    # 定义颜色变化显著的阈值
    color_change_threshold = 10  # 可以根据实际情况调整

    # 记录上一行的像素值
    previous_pixel_value = None

    start_column = int(width/2)
    # 从上到下遍历中间列像素
    for y in range(height-1,-1,-1):
        pixel_value = img[y, start_column]  # 获取当前行中间列的像素值
        
        # 计算颜色差异
        if previous_pixel_value is not None:
            color_diff = np.sqrt(np.sum((pixel_value - previous_pixel_value) ** 2))
            
            # 检查颜色变化是否显著
            if color_diff > color_change_threshold:
                print(f"在第 {y} 行发现颜色变化显著，颜色差异为 {color_diff}")
                print(y/height)
                return(y/height)
                break

        
        # 更新上一行的像素值
        previous_pixel_value = pixel_value
    return -1
    
def picGrayDeg(screenshot_path):
    '''
    输入：窗口截图路径
    返回：bool 是否有广告
    '''
    img = cv2.imread(screenshot_path)
    
    height_,width_,channels = img.shape
    img = img[0:height_//4, :]  # 保留图像的上1/4部分
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
    
    if width_ < height_:
        print(below_threshold_ratio)
    #     return below_threshold_ratio
    # else:
    #     return below_threshold_ratio

# click(bindhwnd,[302/587,273/1046])
# input_command = ['ldconsole', 'action','--index', str(n), '--key', 'call.input', '--value',account]
# input_process = subprocess.Popen(input_command, cwd=root_path, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
# input_process.communicate()

# click(bindhwnd,[286/587,346/1046])
# input_command = ['ldconsole', 'action','--index', str(n), '--key', 'call.input', '--value',password]
# input_process = subprocess.Popen(input_command, cwd=root_path, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
# input_process.communicate()

# # time.sleep()
# click(bindhwnd,[75/587,902/1046])

# # time.sleep()
# click(bindhwnd,[294/587,466/1046])

    # time.sleep()
# while True:
#     time.sleep(0.1)
#     path = printscreen()
#     r= picGrayDeg(path)

    
input_command = ['ldconsole', 'action','--index', str(n), '--key', 'call.input', '--value',password]
input_process = subprocess.Popen(input_command, cwd=root_path, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
input_process.communicate()
    
input('输入内容以结束')