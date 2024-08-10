
import ast
import json
import subprocess
import sys
import time
from Ldconsole import LDconsole
from window import Window,count_pixels_below_threshold, go,countdown
from positionSwitch import convert_to_android_adb_format
import math

# positions = [[120.097076,29.298585],
#               [120.096862,29.298641],
#               [120.09677,29.298803],
#               [120.096822,29.299404],
#               [120.09691,29.299992],
#               [120.096996,29.300147],
#               [120.097219,29.300196],
#               [120.097485,29.300155],
#               [120.097568,29.300008],
#               [120.097537,29.299364],
#               [120.097439,29.298693],
#               [120.097314,29.298593],
#               [120.097097,29.298572]]

# id = 1
print("Processing started")
id = sys.argv[1]
positions = ast.literal_eval(sys.argv[2])


with open('Setting.json', 'r') as f:
    data = json.load(f)
    vms_config = data['vms_config']
    root_path = data['root']

#构造模拟器控制器
Ld = LDconsole(root_path)
Ld.globalSetting( fps = 60, audio =1, fastplay =1, cleanmode =1)
index = int(id)
print(index)
list3 = Ld.list3()

def haversine(lon1, lat1, lon2, lat2):
    """
    Calculate the great circle distance between two points 
    on the earth (specified in decimal degrees)
    """
    # convert decimal degrees to radians 
    lon1, lat1, lon2, lat2 = map(math.radians, [lon1, lat1, lon2, lat2])
    # haversine formula 
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
    c = 2 * math.asin(math.sqrt(a)) 
    km = 6367 * c
    return km
def interpolate(lon1, lat1, lon2, lat2, fraction):
    lon = lon1 + (lon2 - lon1) * fraction
    lat = lat1 + (lat2 - lat1) * fraction
    return lon, lat
def simulate_route_fixed_step(coordinates, speed_kmh, frequency_hz, max_distance_km):
    step_distance_km = speed_kmh / 3600 / frequency_hz  # 每次更新的距离（单位：千米）
    total_distance = 0
    current_position = coordinates[0]
    coord_index = 0
    total_points = len(coordinates)
    
    while total_distance < max_distance_km:
        lon1, lat1 = current_position
        lon2, lat2 = coordinates[(coord_index + 1) % total_points]
        segment_distance = haversine(lon1, lat1, lon2, lat2)
        
        if segment_distance == 0:
            coord_index = (coord_index + 1) % total_points
            continue
        
        num_steps = int(segment_distance / step_distance_km)
        for step in range(num_steps):
            if total_distance >= max_distance_km:
                break
            
            fraction = step / num_steps
            new_lon, new_lat = interpolate(lon1, lat1, lon2, lat2, fraction)
            lng, lat = convert_to_android_adb_format(new_lon, new_lat)
            Ld.actionOfLocate(index,lng, lat)
            Ld.actionOfShake(index)
            
            total_distance += step_distance_km
            current_position = (new_lon, new_lat)
            
            time.sleep(1 / frequency_hz)
        
        coord_index = (coord_index + 1) % total_points

#启动模拟器
print('已开始启动模拟器:',Ld.launch(index))
for i in range(200):
    list3 = Ld.list3()
    EnteredSystem = list3[index]['是否进入android']
    if EnteredSystem:
        print("成功进入安卓系统")
        break
    else:
        time.sleep(1)



new_lon, new_lat = positions[0]       
lng, lat = convert_to_android_adb_format(new_lon, new_lat)
Ld.actionOfLocate(index,lng, lat)

#启动软件
packagename = 'com.zjwh.android_wh_physicalfitness'
Ld.runApp(index = index,packagename = packagename)

#构造窗口控制器
hwnd_bind = list3[index]['绑定句柄']
hwnd = list3[index]['绑定句柄']
window = Window(hwnd,hwnd_bind)

#点击‘GO!’按钮
while True:
    img = window.capture_screenshot()
    if go(img):
        break
    else:
        time.sleep(0.1) 

while True:
    if window.isScreenHorizontal():
        break
    else:
        Ld.ldsInputTap(index = index, x = 611, y = 1111 )
        print('已点击‘GO!’按钮')
        time.sleep(0.1)

while True:
    img = window.capture_screenshot()
    if countdown(img):
        print("已开始跑步")
        break
    else:
        Ld.ldsInputSwipe(index = index, x1 = 264, y1 = 611, x2 = 1209, y2 = 611 )
        time.sleep(0.1)


simulate_route_fixed_step(positions, 14.46, 8,2.6)       

window.bring_to_front()


