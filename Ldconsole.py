#!/usr/bin/env python
# -*- encoding: utf-8 -*-
import os


class LDconsole:
    '''
    【雷电控制台类】
    version: 9.0
    import该文件会自动实例化为 Dc
    '''

    def __init__( self, installation_path:str ):
        '''
        【构造方法】
        '''
        # if 模拟器安装路径存在性检测
        if os.path.exists(installation_path) is False:
            print('模拟器安装路径不存在！')
        # 获取模拟器安装路径
        self.ins_path = installation_path
        # Dnconsole程序路径
        self.console_path = self.ins_path + r'\ldconsole.exe '
        self.ld_path = self.ins_path + r'\ld.exe '
        # if Dnconsole程序路径检测
        if os.path.exists(self.console_path) is False:
            print('Dnconsole程序路径不存在！\n请确认模拟器安装文件是否完整或模拟器版本是否不符！')
        # adb程序路径
        self.adb_path = self.ins_path + r'\adb.exe '
        # if adb程序路径检测
        if os.path.exists(self.adb_path) is False:
            print('Dnconsole程序路径不存在！\n请确认模拟器安装文件是否完整！')
        # 模拟器截屏程序路径
        self.screencap_path = r'/system/bin/screencap'
        # 模拟器截图保存路径
        self.devicess_path = r'/sdcard/autosS.png'
        # 本地图片保存路径
        self.images_path = r'D:\PycharmWorkspace\images'
        # 构造完成
        print('Class-Dnconsole is ready.(%s)' % (self.ins_path))

    def CMD( self, cmd:str ):
        '''
        【执行控制台命令语句】
        :param cmd: 命令
        :return: 控制台调试内容
        '''
        CMD = self.console_path + cmd # 控制台命令
        process = os.popen(CMD)
        result = process.read()
        process.close()
        return result


    def ADB( self, cmd:str ):
        '''
        【执行ADB命令语句】
        :param cmd: 命令
        :return: 控制台调试内容
        '''
        CMD = self.adb_path + cmd # adb命令
        process = os.popen(CMD)
        result = process.read()
        process.close()
        return result
    
    def CMD_ld(self, cmd:str ):
        CMD = self.ld_path + cmd # 控制台命令
        process = os.popen(CMD)
        result = process.read()
        process.close()
        return result

    def quit( self, index:int = 0 ):
        '''
        【关闭模拟器】
        :param index: 模拟器序号
        '''
        cmd = 'quit --index %d' %(index)
        self.CMD(cmd)


    def quitall(self):
        '''
        【关闭所有模拟器】
        '''
        cmd = 'quitall'
        self.CMD(cmd)

    def launch( self, index:int = 0 ):
        '''
        【启动模拟器】
        :param index: 模拟器序号
        :return: True=已启动 / False=不存在
        '''
        cmd = 'launch --index %d' %(index)
        if self.CMD(cmd) == '': return True
        else: return False

    def reboot( self, index:int = 0 ):
        '''
        【重启模拟器】
        :param index: 模拟器序号
        :return: 控制台调试内容
        '''
        cmd = 'reboot --index %d' %(index)
        return self.CMD(cmd)

    def list(self):
        '''
        【获取模拟器列表（仅标题）】
        :return: 控制台调试内容
        '''
        cmd = 'list'
        return self.CMD(cmd)

    def runninglist(self):
        '''
        【获取正在运行的模拟器列表（仅标题）】
        :return: 控制台调试内容
        '''
        cmd = 'runninglist'
        return self.CMD(cmd)


    def isrunning( self, index:int = 0 ):
        '''
        【检测模拟器是否启动】
        :param index: 模拟器序号
        :return: True=已启动 / False=未启动
        '''
        cmd = 'isrunning --index %d' %(index)
        if self.CMD(cmd) == 'running': return True
        else: return False

    def list2(self):
        '''
        【取模拟器列表】
        :return: 列表（索引、标题、顶层句柄、绑定句柄、是否进入android、进程PID、VBox进程PID）
        '''
        cmd = 'list2'
        return self.CMD(cmd)
    
    def list3(self):
        data_str = self.list2()
        lines = data_str.strip().split('\n')
        formatted_data = {}
        
        for line in lines:
            parts = line.split(',')
            entry = {
                '索引': int(parts[0]),
                '标题': parts[1],
                '顶层句柄': int(parts[2]),
                '绑定句柄': int(parts[3]),
                '是否进入android': int(parts[4]),
                '进程PID': int(parts[5]),
                'VBox进程PID': int(parts[6]),
                '分辨率': (int(parts[7]), int(parts[8])),
                '密度': int(parts[9])
            }
            formatted_data[entry['索引']] = entry
        
        return formatted_data

    def add( self, name:str ):
        '''
        【添加模拟器】
        :param name: 新模拟器标题
        :return: 控制台调试内容
        '''
        cmd = 'add %s' %(name)
        return self.CMD(cmd)


    def copy( self, name:str, index:int ):
        '''
        【复制模拟器】
        :param name: 新模拟器标题
        :param index: 原模拟器序号
        :return: 控制台调试内容
        '''
        if not name:
            cmd = 'copy --from %d' %(index)
        else:
            cmd = 'copy --name %s --from %d' %(name, index)
        return self.CMD(cmd)


    def remove( self, index:int ):
        '''
        【移除模拟器】
        :param index: 模拟器序号
        :return: 控制台调试内容
        '''
        cmd = 'remove --index %d' %(index)
        return self.CMD(cmd)


    def rename( self, index:int, newtitle:str ):
        '''
        【重命名模拟器】
        :param index: 模拟器序号
        :param newtitle: 模拟器新标题
        :return: 控制台调试内容
        '''
        cmd = 'rename --index %d --title %s' %(index, newtitle)
        return self.CMD(cmd)

    def modifyResolution( self, index:int, width, height, dpi ):
        '''
        【修改模拟器配置 - 分辨率】
        :param index: 模拟器序号
        :param width: 显示宽度
        :param height: 显示高度
        :param dpi: 每英寸点数
        :return: 控制台调试内容
        '''
        cmd = 'modify --index %d --resolution %s,%s,%s' %(index, width, height, dpi)
        return self.CMD(cmd)


    def modifyCPU( self, index:int, cpu, memory ):
        '''
        【修改模拟器配置 - CPU与内存】
        :param index: 模拟器序号
        :param cpu: 模拟器CPU数量（1，2，3，4）
        :param memory: 模拟器内存大小（256，512，768，1024，1536，2048，3072，4096，6144，8192）
        :return: 控制台调试内容
        '''
        cmd = 'modify --index %d --cpu %s --memory %s' %(index, cpu, memory)
        return self.CMD(cmd)


    def modifyManufacturer( self, index:int, manufacturer, model, pnumber ):
        '''
        【修改模拟器配置 - 制造商信息】
        :param index: 模拟器序号
        :param manufacturer: 制造商
        :param model: 型号
        :param pnumber: 电话号码
        :return: 控制台调试内容
        '''
        cmd = 'modify --index %d --manufacturer %s --model %s --pnumber %s' %(index, manufacturer, model, pnumber)
        return self.CMD(cmd)


    def modifyOthers( self, index:int, autorotate, lockwindow, root ):
        '''
        【修改模拟器配置 - 其他选项】
        :param index: 模拟器序号
        :param autorotate: 自动旋转（1/0）
        :param lockwindow: 锁定窗口（1/0）
        :param root: ROOT（1/0）
        :return: 控制台调试内容
        '''
        cmd = 'modify --index %d --autorotate %s --lockwindow %s --root %s' %(index, autorotate, lockwindow, root)
        return self.CMD(cmd)

    def installappOfFile( self, index:int, filename:str ):
        '''
        【安装App（用文件名）】
        :param index: 模拟器序号
        :param filename: 文件名
        :return: 控制台调试内容
        '''
        cmd = 'installapp --index %d --filename %s' %(index, filename)
        return self.CMD(cmd)


    def installappOfPkg( self, index:int, packagename:str):
        '''
        【安装App（用包名）】
        :param index: 模拟器序号
        :param packagename: 包名
        :return: 控制台调试内容
        '''
        cmd = 'installapp --index %d --packagename %s' %(index, packagename)
        return self.CMD(cmd)


    def uninstallapp( self,index:int, packagename:str ):
        '''
        【卸载App】
        :param index: 模拟器序号
        :param packagename: 包名
        :return: 控制台调试内容
        '''
        cmd = 'uninstallapp --index %d --packagename %s' %(index, packagename)
        return self.CMD(cmd)


    def runApp( self, index:int, packagename:str ):
        '''
        【运行App】
        :param index: 模拟器序号
        :param packagename: 包名
        :return: 控制台调试内容
        '''
        cmd = 'runapp --index %d --packagename %s' %(index, packagename)
        return self.CMD(cmd)


    def killApp( self, index:int, packagename:str ):
        '''
        【终止App】
        :param index: 模拟器序号
        :param packagename: 包名
        :return: 控制台调试内容
        '''
        cmd = 'killapp --index %d --packagename %s' %(index, packagename)
        return self.CMD(cmd)

    def actionOfInput( self, index:int, text:str ):
        '''
        【输入操作】
        :param index: 模拟器序号
        :param text: 文本内容
        :return: 控制台调试内容
        '''
        cmd = 'action --index %d --key call.input --value "%s"' %(index, text)
        return self.CMD(cmd)


    def actionOfKeyboard( self, index:int, key:str ):
        '''
        【按键操作】
        :param index: 模拟器序号
        :param key: 键值（back，home，menu，volumeup，volumedown）
        :return: 控制台调试内容
        '''
        cmd = 'action --index %d --key call.keyboard --value %s' %(index, key)
        return self.CMD(cmd)


    def actionOfShake( self, index:int ):
        '''
        【摇一摇操作】
        :param index: 模拟器序号
        :return:
        '''
        cmd = 'action --index %d --key call.shake --value null' %(index)
        return self.CMD(cmd)


    def actionOfRebootApp(self,index:int, packagename:str):
        '''
        【重启模拟器和App】
        :param index: 模拟器序号
        :param packagename: 包名
        :return: 控制台调试内容
        '''
        cmd = 'action --index %d --key call.reboot --value %s' %(index, packagename)
        return self.CMD(cmd)


    def actionOfLocate( self, index:int, Lng, Lat ):
        '''
        【定位操作】
        :param index: 模拟器序号
        :param Lng: 经度
        :param Lat: 维度
        :return: 控制台调试内容
        '''
        cmd = 'action --index %d --key call.locate --value %f,%f' %(index, Lng, Lat)
        return self.CMD(cmd)


    def actionOfNetwork( self, index:int, ifconnect:bool ):
        '''
        【网络断连操作】
        :param index: 模拟器序号
        :param ifconnect: 是否连网（True/False）
        :return: 控制台调试内容
        '''
        if ifconnect:
            cmd = 'action --index %d --key call.network --value connect' %(index)
        else:
            cmd = 'action --index %d --key call.network --value offline' %(index)
        return self.CMD(cmd)


    def actionOfGravity(self, index:int, x:int, y:int, z:int):
        '''
        【改变重力感应操作】
        :param index: 模拟器序号
        :param x: x
        :param y: y
        :param z: z
        :return: 控制台调试内容
        '''
        cmd = 'action --index %d --key call.gravity --value %d,%d,%d' %(index, x, y, z,)
        return self.CMD(cmd)


    def scan( self, index:int, filepath:str ):
        '''
        【扫描二维码】
        :param index: 模拟器序号
        :param filepath: 图片路径
        :return: 控制台调试内容
        '''
        cmd = 'scan  --index %d --file %s' %(index, filepath)
        return self.CMD(cmd)

    def sortWnd(self):
        '''
        【对模拟器窗口排版】
        '''
        cmd = 'sortWnd'
        self.CMD(cmd)

    def pull( self, index:int, remote:str, local:str ):
        '''
        【复制文件】
        :param index: 模拟器序号
        :param remote: 模拟器文件路径
        :param local: 本地路径
        :return: 控制台调试内容
        '''
        cmd = 'pull  --index %d --remote %s --local %s' %(index, remote, local)
        return self.CMD(cmd)


    def push( self, index:int, remote:str, local:str ):
        '''
        【发送文件】
        :param index: 模拟器序号
        :param remote: 模拟器文件路径
        :param local: 本地路径
        :return: 控制台调试内容
        '''
        cmd = 'push  --index %d --remote %s --local %s' %(index, remote, local)
        return self.CMD(cmd)

    def globalSetting( self, fps:int, audio:int, fastplay:int, cleanmode:int ):
        '''
        【全局设置】
        :param fps: 帧率（0~60）
        :param audio: 音频（1=开/0=关）
        :param fastplay: 高帧率模式（1=开/0=关）
        :param cleanmode: 除广告模式（1=开/0=关）
        :return: 控制台调试内容
        '''
        cmd = 'globalsetting --fps %d --audio %d --fastplay %d --cleanmode %d' %(fps, audio, fastplay, cleanmode)
        return self.CMD(cmd)

    def launchx( self, index:int, packagename:str ):
        '''
        【同时启动模拟器和App】
        :param index: 模拟器序号
        :param packagename: 包名
        :return: 控制台调试内容
        '''
        cmd = 'launchex --index %d --packagename "%s"' %(index, packagename)
        return self.CMD(cmd)

    def device(self):
        '''
        【列出所有连接的设备】
        :return: 控制台调试内容
        '''
        cmd = 'devices -l'
        return self.ADB(cmd)

    def connect( self, ip:str, port:str ):
        '''
        【连接设备】
        :param ip: ip地址
        :param port: 端口号
        :return: 控制台调试内容
        '''
        cmd = 'connect %s:%s' %(ip, port)
        return self.ADB(cmd)


    def disconnect( self, ip:str, port:str ):
        '''
        【断开设备】
        :param ip: ip地址
        :param port: 端口号
        :return: 控制台调试内容
        '''
        if ip != '' and port != '':
            cmd = 'disconnect %s:%s' %(ip, port)
        elif ip != '' and port == '':
            cmd = 'disconnect %s' %(ip)
        else:
            cmd = 'disconnect'
        return self.ADB(cmd)

    def versionOfADB(self):
        '''
        【查看ADB版本号】
        :return: 控制台调试内容
        '''
        cmd = 'version'
        return self.ADB(cmd)

    def dumpstate( self, index:int ):
        '''
        【获取设备系统状态信息（需要root权限）】
        :param index: 模拟器序号
        :return: 控制台调试内容
        '''
        cmd = 'adb --index %d --command "shell dumpstate"' %(index)
        return self.CMD(cmd)


    def getPackageList( self, index:int ):
        '''
        【获取设备包名列表】
        :param index: 模拟器序号
        :return: 包名列表
        '''
        cmd = 'adb --index %d --command "shell pm list package"' %(index)
        return self.CMD(cmd)


    def getResolution( self, index:int ):
        '''
        【获取设备分辨率】
        :param index: 模拟器序号
        :return: 分辨率（例如'1920x1080'）
        '''
        cmd = 'adb --index %d --command "shell wm size"' %(index)
        return self.CMD(cmd).replace('Physical size: ', '')

    def screenShot ( self, index:int ):
        '''
        【截屏并保存到本地】
        :param index: 模拟器序号
        '''
        cmd1 = 'adb --index %d --command "shell %s -p %s"' %(index, self.screencap_path, self.devicess_path)
        cmd2 = 'adb --index %d --command "pull %s %s"' %(index, self.devicess_path, self.images_path)
        self.CMD(cmd1)
        self.CMD(cmd2)

    def appVersion( self, index:int, packagename:str ):
        '''
        【获取App版本号】
        :param index: 模拟器序号
        :param packagename: 包名
        :return: 控制台调试内容
        '''
        cmd = 'adb --index %d --command "shell dumpsys package %s|grep versionName"' %(index, packagename)
        return self.CMD(cmd)


    def appIsrunning( self, index:int, packagename:str ):
        '''
        【获取App运行状态】
        :param index: 模拟器序号
        :param packagename: 包名
        :return: 控制台调试内容
        '''
        cmd = 'adb --index %d --command "shell pidof %s"' %(index, packagename)
        return self.CMD(cmd)

    def actionOfTap( self, index:int, x:int, y:int ):
        '''
        【点击操作】
        :param index: 模拟器序号
        :param x: x
        :param y: y
        :return: 控制台调试内容
        '''
        cmd = 'adb --index %d --command "shell input tap %d %d"' %(index, x, y)
        return self.CMD(cmd)
    
    def ldsInputTap( self, index:int, x:int, y:int ):
        '''
        【点击操作】
        :param index: 模拟器序号
        :param x: x
        :param y: y
        :return: 控制台调试内容
        '''
        cmd = '-s %d input tap %d %d"' %(index, x, y)
        return self.CMD_ld(cmd)


    def actionOfSwipe( self, index:int, x0:int, y0:int, x1:int, y1:int, ms:int = 200 ):
        '''
        【滑动操作】
        :param index: 模拟器序号
        :param x0,y0: 起点坐标
        :param x1,y1: 终点坐标
        :param ms: 滑动时长
        :return: 控制台调试内容
        '''
        cmd = 'adb --index %d --command "shell input swipe %d %d %d %d %d"' %(index, x0, y0, x1, y1, ms)
        return self.CMD(cmd)
    
    def ldsInputSwipe( self, index:int, x1:int, y1:int ,x2:int,y2:int):
        '''
        【点击操作】
        :param index: 模拟器序号
        :param x: x
        :param y: y
        :return: 控制台调试内容
        '''
        cmd = '-s %d input swipe %d %d %d %d"' %(index, x1, y1, x2, y2)
        return self.CMD_ld(cmd)

    def actionOfKeyCode( self, index:int, keycode:int ):
        '''
        【键码输入操作】
        :param index: 模拟器序号
        :param keycode: 键码（0~9，10=空格）
        :return: 控制台调试内容
        '''
        try:
            list = ['KEYCODE_0', 'KEYCODE_1', 'KEYCODE_2', 'KEYCODE_3', 'KEYCODE_4', 'KEYCODE_5',
                    'KEYCODE_6', 'KEYCODE_7', 'KEYCODE_8', 'KEYCODE_9', 'KEYCODE_HOME']
            cmd = 'adb --index %d --command "shell input keyevent %s"' %(index, list[keycode])
            return self.CMD(cmd)
        except Exception as e:
            print(e)
