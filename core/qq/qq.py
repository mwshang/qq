#coding=utf-8

import win32gui
import win32api
import win32con
import clipboard
import os;
import time;

from pykeyboard import PyKeyboard
from ctypes import *
from core.utils.config import QQ_PATH

class QQ:
    '''
        account:账号密码{qq,pwd}

    '''
    def __init__(self,account,mgr):
        self.account = account;
        self.mgr = mgr;
        self.pinfo = [];
        self.state = 0;

    def getPId(self):
        if len(self.pinfo) > 0:
            return self.pinfo[0]["pid"];
        return -1;

    def getQQNum(self):
        return self.account["qq"];

    '''
        pinfo:系统进程信息[{pid,name}]
    '''
    def setPInfo(self,pinfo):
        self.pinfo = pinfo;

    def isLogined(self):
        return self.state == 1;

    def sendMsg(self,msg,targetName):
        clipboard.copy(msg);
        hwnd = win32gui.FindWindow(None,targetName)
        if hwnd > 0 :
            #win32gui.SetForegroundWindow(hwnd)  # 指定句柄设置为前台，也就是激活
            #win32gui.SetBkMode(hwnd, win32con.TRANSPARENT)# 设置为后台
            # 填充消息
            win32gui.SendMessage(hwnd, 770, 0, 0);
            # 回车发送消息
            win32gui.SendMessage(hwnd, win32con.WM_KEYDOWN, win32con.VK_RETURN, 0);

    # 登录QQ
    def loginQQ(self):
        qq = self.account['qq'];
        pwd = self.account['pwd'];
        # 运行QQ
        os.system(QQ_PATH);
        time.sleep(5)
        # 获取QQ的窗口句柄
        # 参数1是类名,参数2是QQ软件的标题
        a = win32gui.FindWindow(None, "QQ")
        # 获取QQ登录窗口的位置
        loginid = win32gui.GetWindowPlacement(a)
        #print(loginid)
        #print(loginid[4][0])
        #print(loginid[4][1])

        # 定义一个键盘对象
        k = PyKeyboard()

        # 把鼠标放置到登陆框的输入处
        windll.user32.SetCursorPos(loginid[4][0] + 192, loginid[4][1] + 245)

        # 按下鼠标再释放
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)  # press mouse
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)  # release mouse

        time.sleep(2)
        ###input username
        # 输入用户名
        k.type_string(qq)
        time.sleep(0.5)
        ##tab
        # 按下tab，切换到输入密码的地方
        win32api.keybd_event(9, 0, 0, 0)
        win32api.keybd_event(9, 0, win32con.KEYEVENTF_KEYUP, 0)
        # 按下tab用下面两行也行
        # k.press_key(k.tab_key)
        # k.release_key(k.tab_key)
        # 按下tab用下面一行也行
        # k.tap_key(k.tab_key)

        # 输入密码
        k.type_string(pwd)
        time.sleep(0.5)

        # 按下回车
        win32api.keybd_event(13, 0, 0, 0);
        win32api.keybd_event(13, 0, win32con.KEYEVENTF_KEYUP, 0);

        # 最小化没啥用
        Minimize = win32gui.GetForegroundWindow()  # 获取窗口句柄
        win32gui.ShowWindow(Minimize, win32con.SW_MINIMIZE)  # 最小化
        self.state = 1;

        time.sleep(2);

        self.setPInfo(self.mgr.getANewPid());

        return True;

    #关闭所有QQ
    def close(self):
        #os.system('taskkill /f /im QQ.exe');
        self.state = 0;
        if len(self.pinfo) > 0:
            for p in self.pinfo:
                cmd = "taskkill /pid {0} /f".format(p["pid"]);
                os.system(cmd);

            print("successed to close qq:{0} pid:{1}".format(self.account["qq"], self.pinfo[0]["pid"]))
            self.pinfo = [];
        else:
            print("error:qq:{0}'s pid is none,close failed!!!!".format(self.account["qq"]));