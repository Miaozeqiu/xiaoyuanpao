import cv2
import numpy as np
from PIL import ImageGrab
import win32gui
# 捕捉指定窗口的图像
def capture_window(hwnd):
    rect = win32gui.GetWindowRect(hwnd)
    img = ImageGrab.grab(bbox=rect)
    img_np = np.array(img)
    return cv2.cvtColor(img_np, cv2.COLOR_BGR2RGB)

# 处理图像并识别元素
def process_image(img):
    # 将图像转换为灰度
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # 检测边缘
    edges = cv2.Canny(gray, 100, 200)
    # 显示图像
    cv2.imshow("Edges", edges)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

# 获取窗口句柄
hwnd = win32gui.FindWindow(None, "雷电多开器")
if hwnd:
    img = capture_window(hwnd)
    process_image(img)
else:
    print("窗口未找到")