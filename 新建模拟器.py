import json
import subprocess
import os
import re
from ldconsolefunc import list2
from ldconsolefunc import get_window_size
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
print(n)


s= input('请输入姓名：')
# 定义目录路径
# directory_path = root_path

# 构造命令和参数
add_command = ['ldconsole.exe', 'add','--name',s]

# 使用subprocess.Popen执行命令
add_process = subprocess.Popen(add_command, cwd=root_path, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
add_process.communicate()
modify_command = ['ldconsole.exe', 'modify','--name',s,'--root','1']
modify_process = subprocess.Popen(modify_command, cwd=root_path, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
modify_process.communicate()
# # 获取命令输出和错误信息
# output, error = process.communicate()

# # 打印命令执行结果
# if process.returncode == 0:
#     print(f"Command executed successfully:\n{output.decode('utf-8')}")
# else:
#     print(f"Command failed with error:\n{error.decode('utf-8')}")


config_file = os.path.join(vms_config, 'leidian'+str(n)+'.config')

# 1. 读取 JSON 文件
with open(config_file, 'r', encoding='utf-8') as f:
    config = json.load(f)

# 2. 修改参数
config['basicSettings.standaloneSysVmdk'] = True

# 3. 写回文件
with open(config_file, 'w', encoding='utf-8') as f:
    json.dump(config, f, indent=4)

print("File updated successfully.")


launch_command = ['ldconsole', 'installapp','--name',s,'--filename',r'C:\Users\Administrator\Downloads\Compressed\狐狸面具+LSPosed等3个文件\狐狸面具+LSPosed\狐狸面具_v26.4.apk']
launch_process = subprocess.Popen(launch_command, cwd=root_path, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
launch_process.communicate()

# run_command = ['ldconsole', 'runapp','--name',s,'--packagename','Kitsune Musk']
# run_process = subprocess.Popen(run_command, cwd=root_path, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
# run_process.communicate()
# print('signal')

vmList =list2(root_path)
bindhwnd = vmList[n]['bindhwnd']
def click(hwnd,wh_r):
    w,h = get_window_size(hwnd)
    w*=wh_r[0]
    h = wh_r[1]
    click_command = ['ld', '-s', n, 'input', 'tap', int(w),int(h)]
    click_process = subprocess.Popen(click_command, cwd=root_path, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    click_process.communicate()
click(bindhwnd,[597/1357,206/765])
input()