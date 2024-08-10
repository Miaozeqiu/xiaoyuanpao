import cv2
import numpy as np

def detect_white_circle(image_path):
    # 读取图像
    image = cv2.imread(image_path)
    if image is None:
        print("Cannot read the image.")
        return False
    
    # 转换为灰度图像
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # 使用高斯模糊平滑图像
    blurred = cv2.GaussianBlur(gray, (9, 9), 2)
    
    # 使用Canny边缘检测
    edges = cv2.Canny(blurred, 50, 150)
    
    # 检测圆圈
    circles = cv2.HoughCircles(edges, cv2.HOUGH_GRADIENT, dp=1.2, minDist=50,
                               param1=50, param2=30, minRadius=10, maxRadius=100)
    
    # 如果检测到圆圈
    if circles is not None:
        circles = np.round(circles[0, :]).astype("int")
        
        for (x, y, r) in circles:
            # 提取圆圈区域
            mask = np.zeros_like(gray)
            cv2.circle(mask, (x, y), r, 255, -1)
            mean_val = cv2.mean(gray, mask=mask)[0]
            
            # 判断圆圈是否为白色
            if mean_val > 200:  # 根据图像调整阈值
                print(f"Detected white circle at ({x}, {y}) with radius {r}.")
                return True
    
    print("No white circle detected.")
    return False

# 示例调用
image_path = 'output.jpg'
detect_white_circle(image_path)
