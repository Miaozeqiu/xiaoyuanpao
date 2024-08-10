import math
import random
import subprocess
import time
import threading
import win32gui
import win32api
import win32con
root_path = r'C:\leidian\LDPlayer9'
n = '1'
import pyautogui
import pygetwindow as gw
from Ldconsole import LDconsole
ld = LDconsole('C:\leidian\LDPlayer9')
# 获取窗口句柄
hwnd = 3017432  # 这里替换成你具体的窗口句柄

# 激活窗口
# win32gui.SetForegroundWindow(hwnd)



from positionSwitch import convert_to_android_adb_format
positions = [[120.097076,29.298585],
              [120.096862,29.298641],
              [120.09677,29.298803],
              [120.096822,29.299404],
              [120.09691,29.299992],
              [120.096996,29.300147],
              [120.097219,29.300196],
              [120.097485,29.300155],
              [120.097568,29.300008],
              [120.097537,29.299364],
              [120.097439,29.298693],
              [120.097314,29.298593],
              [120.097097,29.298572]]

def setlocation(location):
    cmd = ['ldconsole','action','--index',n,'--key','call.locate','--value',f'{location[0]},{location[1]}']
    process = subprocess.Popen(cmd, cwd=root_path, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    process.communicate()

def setxyz(x,y,z):
    cmd = ['ldconsole','action','--index',n,'--key','call.gravity','--value',f'{x},{y},{z}']
    process = subprocess.Popen(cmd, cwd=root_path, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    process.communicate()
    

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
            setlocation([lng, lat])
            ld.actionOfShake(1)
            
            total_distance += step_distance_km
            current_position = (new_lon, new_lat)
            
            time.sleep(1 / frequency_hz)
        
        coord_index = (coord_index + 1) % total_points

simulate_route_fixed_step(positions, 14.46, 8,999)




int(input())