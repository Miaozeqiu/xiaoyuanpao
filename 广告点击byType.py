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





def printscreen(dlg):

    '''
    对窗口进行截图,返回截图路径 screenshot_path
    '''

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
    '''
    输入：
        image_path,  窗口截图路径
        template_path, 模板路径
        threshold=0.8, 相似度阈值
        click = False 是否直接点击
    输出：
        result.png 识别结果，会框起来
    '''
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



#检测广告
def jiance(screenshot_path):
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
    
    if below_threshold_ratio < 0.7 and width_ < height_:
        print("有广告")
        return True
    else:
        return False
    
    
#类型识别
def RecType(input_path):
    '''
    输入：手机屏幕截图路径
    返回：关闭广告按钮的位置
    '''
    Type = {0.97:[399/522,264/930],0.22:[420/566,256/1005],0.10:[82/564,137/1005],0.03:[548/587,93/1046],0.14:[94/525,233/961],0.19:[450/588,296/1046]}

    # 读取彩色图像
    img = cv2.imread(screenshot_path)  # 默认以BGR格式读取

    # 获取图像高度和宽度
    height, width, channels = img.shape

    # 定义要检查的目标像素值（示例：假设为(255, 255, 255)，可以根据实际需求修改）
    target_pixel_value = (31,23,22)
    allowed_error = 0  # 允许的误差范围

    # 遍历第一列像素，从上到下
    for top in range(height):
        pixel_value = img[top, 0]  # 获取第一列当前行的像素值
        
        # 检查每个通道的像素值是否在允许误差范围内
        if all(abs(pixel_value[channel] - target_pixel_value[channel]) <= allowed_error for channel in range(channels)):
            continue  # 符合要求，继续下一行
        else:
            #print(f"在第 {y} 行遇到不符合像素值要求的像素，像素值为 {pixel_value}")
            break
    else:
        print("第一列像素全部符合要求")  # 如果没有中断循环，则说明第一列所有像素都符合要求
    for right in range(4,width):
        pixel_value = img[top, right]
        if  all(pixel_value == target_pixel_value):
            right -= 1
            break
        else:
            continue
    crop_image(screenshot_path,'cache_croped.png',[0,top,right,height])
    img = cv2.imread('cache_croped.png')
    # 获取图像高度和宽度
    height, width, channels = img.shape


    # 定义颜色变化显著的阈值
    color_change_threshold = 10  # 可以根据实际情况调整

    # 记录上一行的像素值
    previous_pixel_value = None

    # 从上到下遍历中间列像素
    # for y in range(height-5,-1,-1):
    #     pixel_value = img[y, start_column]  # 获取当前行中间列的像素值
        
    #     # 计算颜色差异
    #     if previous_pixel_value is not None:
    #         color_diff = np.sqrt(np.sum((pixel_value - previous_pixel_value) ** 2))
            
    #         # 检查颜色变化是否显著
    #         if color_diff > color_change_threshold:
    #             print(f"在第 {y} 行发现颜色变化显著，颜色差异为 {color_diff}")
    #             print(y/height)
    #             break
        
    #     # 更新上一行的像素值
    #     previous_pixel_value = pixel_value
    middle_row = height // 2  # 计算图像的中间行

    for x in range(5, width):
        pixel_value = img[middle_row, x]  # 获取中间行当前列的像素值
        
        # 计算颜色差异
        if previous_pixel_value is not None:
            color_diff = np.sqrt(np.sum((pixel_value - previous_pixel_value) ** 2))
            
            # 检查颜色变化是否显著
            if color_diff > color_change_threshold:
                print(f"在第 {middle_row} 行第 {x} 列发现颜色变化显著，颜色差异为 {color_diff}")
                print(f"中间行比例: {x / width}")
                break
        
        # 更新上一列的像素值
        previous_pixel_value = pixel_value
    else:
        print("中间列像素变化不显著")
    

    n = -1
    for i in Type.keys():
        if abs(x/width-i)<=0.01:
            n = i
            break
    if n != -1:
        buttonw, buttonh = Type[n]
        buttonh *= height 
        buttonh += top-1
        buttonw *= width
        return buttonw, buttonh
    else:
        return [-1,-1]
    #crop_image('cache_croped.png','cache_croped_croped.png',[0,y,right,height])      



#广告点击
def CloseAd(screenshot_path,dlg):
    buttonw, buttonh = RecType(screenshot_path)
    if buttonw != -1:
        pass
        dlg.click_input(coords=(int(buttonw), int(buttonh)))
            
if __name__ == '__main__':     
    app = Application().connect(title="雷电模拟器-3")
    dlg = app.window(title="雷电模拟器-3")
    dlg.set_focus()
    #send_keys('{VK_F9}')  #震动
    # process = []

    # 进行元素识别和点击
    # screenshot_path = printscreen()
    # # 模板图片路径（假设你有一个按钮模板）
    # template_path = os.path.join(os.getcwd(), "moniqi", "YDXYSJ_.jpg")
    # recognize_elements(screenshot_path, template_path,click = True)
    while True:
        time.sleep(0.05)
        screenshot_path = printscreen(dlg = dlg)
        if(jiance(screenshot_path)):
            CloseAd(screenshot_path,dlg=dlg)
            