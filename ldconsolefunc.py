import json
import subprocess
import ctypes
import win32gui


def parse_list2_output(output):
    lines = output.decode('gbk').strip().split('\r\n')
    vm_list = []
    for line in lines:
        fields = line.split(',')
        if len(fields) < 9:
            continue  # Skip lines that don't have enough fields
        try:
            vm_info = {
                'index': fields[0],
                'name': fields[1],  # 第二个字段是虚拟机名称
                'tophwnd': fields[2],
                'bindhwnd': fields[3], #手机画面句柄
                'status': int(fields[6]),  # 第七个字段是状态
                'resolution': {
                    'width': int(fields[7]),  # 第八个字段是宽度
                    'height': int(fields[8])  # 第九个字段是高度
                }
            }
            vm_list.append(vm_info)
        except ValueError:
            continue  # Skip lines with invalid integer fields
    return vm_list

def list2(root_path):
    list2_command = ['ldconsole', 'list2']
    list2_process = subprocess.Popen(list2_command, cwd=root_path, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    stdout, stderr = list2_process.communicate()
    
    if list2_process.returncode != 0:
        print(f"Error executing ldconsole list2: {stderr.decode('utf-8')}")
        return None
    
    vm_list = parse_list2_output(stdout)
    
    # Convert vm_list to dictionary with indices as keys
    vm_dict = {vm['index']: vm for vm in vm_list}
    return vm_dict




def get_window_size(hwnd):
    # 函数声明
    user32 = ctypes.windll.user32
    GetWindowRect = user32.GetWindowRect
    # 获取窗口矩形信息
    rect = ctypes.wintypes.RECT()
    GetWindowRect(hwnd, ctypes.byref(rect))
    
    # 计算窗口大小
    width = rect.right - rect.left
    height = rect.bottom - rect.top
    
    return (width, height)


def get_window_size(hwnd):
    try:
        # Get the window's rect: (left, top, right, bottom)
        rect = win32gui.GetWindowRect(hwnd)
        # Calculate width and height
        width = rect[2] - rect[0]
        height = rect[3] - rect[1]
        return width, height
    except Exception as e:
        print(f"An error occurred: {e}")
        return None, None

def click(hwnd,wh_r):
    
    w = 720
    h = 1280
    print(w,h)
    w*=wh_r[0]
    h*= wh_r[1]
    click_command = ['ld', '-s', '9', 'input', 'tap', str(int(w)),str(int(h))]
    click_process = subprocess.Popen(click_command, cwd=root_path, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    click_process.communicate()

if __name__ == "__main__":
    
    # 从 Setting.json 文件中读取 root_path
    with open('Setting.json', 'r') as f:
        data = json.load(f)
        root_path = data['root']

    # 调用 list2 函数获取虚拟机列表信息
    vm_list = list2(root_path)

    # if vm_list:
    #     print("Virtual Machine List:")
    #     for idx, vm in enumerate(vm_list):
    #         print(f"VM {idx}:")
    #         print(f"  Name: {vm['name']}")
    #         print(f"  Status: {vm['status']}")
    #         print(f"  Resolution: {vm['resolution']['width']} x {vm['resolution']['height']}")
    #         print()
    bindhwnd = vm_list['9']['tophwnd']
    print(bindhwnd)
    # print(get_window_size(bindhwnd))
    # print(f"System DPI scaling is set to: {dpi_scaling}%")


    # 示例用法：获取句柄为 852422 的窗口大小
    # hwnd = 1575400  # 替换成你要获取大小的窗口句柄
    size = get_window_size(bindhwnd)
    if size:
        # print(f"Window with handle {hwnd} size: {int(size[0]/dpi_scaling*100)} x {int(size[1]/dpi_scaling*100)} pixels")
        print(f"Window with handle {bindhwnd} size: {size[0]*1.25} x {size[1]*1.25} pixels")

    # click(bindhwnd,[597/1357,206/765])


