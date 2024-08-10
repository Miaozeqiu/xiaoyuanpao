import json
import sys
import subprocess
import os
import re
import cv2
import numpy as np
from ldconsolefunc import list2
from ldconsolefunc import get_window_size
import time
from pywinauto import Application
with open('Setting.json', 'r') as f:
    data = json.load(f)
    vms_config = data['vms_config']
    root_path = data['root']
# print(vms)



# 定义正则表达式模式
pattern = re.compile(r'leidian(\d+)\.config')

# 存储匹配的数字
numbers = []

# 遍历文件夹及其子文件夹
for root, dirs, files in os.walk(vms_config):
    for file in files:
        # 检查文件名是否匹配正则表达式
        match = pattern.match(file)
        if match:
            # 提取数字
            number = match.group(1)
            numbers.append(int(number))

n = 0
# 打印提取的数字
while True:
    if n not in numbers:
        break
    else:
        n+=1
print(f'ID = {n}')

s = sys.argv[1]
account = sys.argv[2]
password = sys.argv[3]
# s= input('请输入姓名：')
# account = input('请输入账户：')
# password = input('请输入密码：')
# 定义目录路径
# directory_path = root_path

# 构造命令和参数
add_command = ['ldconsole.exe', 'add','--name',s]
add_process = subprocess.Popen(add_command, cwd=root_path, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
add_process.communicate()

launch_command = ['ldconsole', 'installapp','--name',s,'--filename',r'C:\Users\Administrator\Downloads\运动世界校园.APK']
launch_process = subprocess.Popen(launch_command, cwd=root_path, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
launch_process.communicate()

while True:
    vmList =list2(root_path)
    bindhwnd = vmList[str(n)]['bindhwnd']
    time.sleep(2)
    run_command = ['ldconsole', 'runapp','--name',s,'--packagename','com.zjwh.android_wh_physicalfitness']
    run_process = subprocess.Popen(run_command, cwd=root_path, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    run_process.communicate()
    w,h = get_window_size(bindhwnd)
    if not h:
        continue
    if h > w:
        break

#权限给予
def Permission(permission):
    command = ['ld', '-s',str(n),'pm','grant','com.zjwh.android_wh_physicalfitness',permission]
    process = subprocess.Popen(run_command, cwd=root_path, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    process.communicate()
permissions = ['android.permission.WRITE_EXTERNAL_STORAGE',
               'android.permission.CALL_PHONE',
               'android.permission.BODY_SENSORS',
               'android.permission.ACCESS_FINE_LOCATION',
               'android.permission.ACCESS_FINE_LOCATION','android.permission.ACCESS_COARSE_LOCATION',
               'android.permission.ACTIVITY_RECOGNITION',
               'android.permission.SYSTEM_ALERT_WINDOW']

for permission in permissions:
    Permission(permission)


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
        return below_threshold_ratio

app = Application().connect(handle=int(bindhwnd))
dlg = app.window(handle=int(bindhwnd))  # 获取具有该句柄的窗口




def printscreen():
    screenshot = dlg.capture_as_image()
    screenshot_path = os.path.join(os.getcwd(), "cache.png")
    screenshot.save(screenshot_path)
    return screenshot_path

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
                # print(f"在第 {y} 行发现颜色变化显著，颜色差异为 {color_diff}")
                # print(y/height)
                return(y/height)
                break

        
        # 更新上一行的像素值
        previous_pixel_value = pixel_value
    return -1

# vmList =list2(root_path)
# bindhwnd = vmList[str(n)]['bindhwnd']
def click(hwnd,wh_r,vertical = True):
    # w,h = get_window_size(hwnd)
    if not vertical:
        w = 1280
        h = 720
    else:
        w = 720
        h = 1280
    w*=wh_r[0]
    h *= wh_r[1]
    click_command = ['ld', '-s', str(n), 'input', 'tap', str(int(w)),str(int(h))]
    click_process = subprocess.Popen(click_command, cwd=root_path, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    click_process.communicate()

while True:
    time.sleep(0.1)
    path = printscreen()
    r= picGrayDeg(path)
    if r< 0.9:
        break

click(bindhwnd,[378/587,835/1042])



while True:
    time.sleep(0.1)
    path = printscreen()
    r= findEdge(path)
    if abs(r-0.87)< 0.01:
        print('进入')
        break


click(bindhwnd,[302/587,273/1046])
input_command = ['ldconsole', 'action','--index', str(n), '--key', 'call.input', '--value',account]
input_process = subprocess.Popen(input_command, cwd=root_path, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
input_process.communicate()

click(bindhwnd,[286/587,346/1046])
input_command = ['ldconsole', 'action','--index', str(n), '--key', 'call.input', '--value',password]
input_process = subprocess.Popen(input_command, cwd=root_path, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
input_process.communicate()

# time.sleep()
click(bindhwnd,[75/587,902/1046])

# time.sleep()
click(bindhwnd,[294/587,466/1046])

exit