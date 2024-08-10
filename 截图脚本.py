from pywinauto import Application
import os
import cv2
import numpy as np

# 截图部分
app = Application().connect(class_name="LDPlayerMainFrame")
dlg = app.window(class_name="LDPlayerMainFrame")
dlg.set_focus()

screenshot = dlg.capture_as_image()
screenshot_path = os.path.join(os.getcwd(), "screenshot.png")
screenshot.save(screenshot_path)
print(f"截图已保存至 {screenshot_path}")


