from pywinauto import Application
import os
import cv2
import numpy as np

# 截图部分
app = Application().connect(class_name="LDRemoteLoginFrame")
dlg = app.window(class_name="LDRemoteLoginFrame")

screenshot = dlg.capture_as_image()
screenshot_path = os.path.join(os.getcwd(), "screenshot.png")
screenshot.save(screenshot_path)
print(f"截图已保存至 {screenshot_path}")

# 图像处理和元素识别部分
def recognize_elements(image_path, template_path, threshold=0.8):
    # 读取截图
    img = cv2.imread(image_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # 读取模板
    template = cv2.imread(template_path, 0)
    w, h = template.shape[::-1]

    # 模板匹配
    res = cv2.matchTemplate(gray, template, cv2.TM_CCOEFF_NORMED)
    loc = np.where(res >= threshold)

    for pt in zip(*loc[::-1]):
        # 绘制识别到的矩形
        cv2.rectangle(img, pt, (pt[0] + w, pt[1] + h), (0, 255, 0), 2)
        
        # 点击识别到的元素
        dlg.click_input(coords=(int(pt[0] + w / 2), int(pt[1] + h / 2)))
        

    result_path = os.path.join(os.getcwd(), "result.png")
    cv2.imwrite(result_path, img)
    print(f"识别结果已保存至 {result_path}")

# 模板图片路径（假设你有一个按钮模板）
template_path = os.path.join(os.getcwd(), "button_template.png")

# 进行元素识别和点击
recognize_elements(screenshot_path, template_path)