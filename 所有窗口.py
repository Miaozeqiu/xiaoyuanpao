import win32gui

def list_window_classes(hwnd, _):
    window_text = win32gui.GetWindowText(hwnd)
    class_name = win32gui.GetClassName(hwnd)
    print(f"Window Handle: {hwnd}, Text: {window_text}, Class: {class_name}")

# 枚举所有顶层窗口
win32gui.EnumWindows(list_window_classes, None)