#!/usr/bin/python

import os
import time
import win32gui
import win32api
import win32con
import pymouse
import clipboard
import psutil
import db;

from pymouse import *
from pykeyboard import PyKeyboard
#import keyboard;
from ctypes import *


qqList = "qq.txt"

class QQ:
    def __init__(self):
        self.dictPids = {}
        self.qqPidName = "QQ.exe";

        self._initData();

    def _initData(self):
        pids = self._collectQQ();
        for pid in pids:
            self.dictPids[pid['pid']] = pid;

    def _collectQQ(self):
        list = []
        for proc in psutil.process_iter():
            try:
                pinfo = proc.as_dict(attrs=['pid', 'name'])
            except psutil.NoSuchProcess:
                pass
            else:
                if pinfo['name'] == self.qqPidName:
                    list.append(pinfo)

        return list;

    # 登录QQ
    def _loginQQ(self,qq,pwd):
        #运行QQ
        os.system('"D:\Program Files (x86)\Tencent\QQ\Bin\QQScLauncher.exe"')
        time.sleep(5)
        #获取QQ的窗口句柄
        #参数1是类名,参数2是QQ软件的标题
        a = win32gui.FindWindow(None,"QQ")
        #获取QQ登录窗口的位置
        loginid = win32gui.GetWindowPlacement(a)
        print (loginid)
        print (loginid[4][0])
        print (loginid[4][1])

        #定义一个键盘对象
        k = PyKeyboard()

        #把鼠标放置到登陆框的输入处
        windll.user32.SetCursorPos(loginid[4][0]+192,loginid[4][1]+245)

        #按下鼠标再释放
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,0,0,0,0)#press mouse
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,0,0,0,0)#release mouse

        time.sleep(2)
        ###input username
        #输入用户名
        k.type_string(qq)
        time.sleep(0.5)
        ##tab
        #按下tab，切换到输入密码的地方
        win32api.keybd_event(9,0,0,0)
        win32api.keybd_event(9,0,win32con.KEYEVENTF_KEYUP,0)
        #按下tab用下面两行也行
        #k.press_key(k.tab_key)
        #k.release_key(k.tab_key)
        #按下tab用下面一行也行
        #k.tap_key(k.tab_key)

        #输入密码
        k.type_string(pwd)
        time.sleep(0.5)

        #按下回车
        win32api.keybd_event(13,0,0,0);
        win32api.keybd_event(13,0,win32con.KEYEVENTF_KEYUP,0);

        #最小化没啥用
        Minimize = win32gui.GetForegroundWindow()            #获取窗口句柄
        win32gui.ShowWindow(Minimize, win32con.SW_MINIMIZE)  # 最小化
        return True;

    def loginQQ(self):
        F = open(qqList, "r").readlines()
        for i in F:
            tx = i.split('----')
            # print (tx[0])#打印用户名
            # print (tx[1])#打印密码
            print("Start to login qq:" + tx[0]);
            while self._loginQQ(tx[0], tx[1]):
                time.sleep(7);
                print("Finished to login qq:" + tx[0]);
                break;
        return True;

    def sendMsg(self,msg,targetName):
        clipboard.copy(msg);
        handle = win32gui.FindWindow(None,targetName)
        if handle > 0 :
            # 填充消息
            win32gui.SendMessage(handle, 770, 0, 0);
            # 回车发送消息
            win32gui.SendMessage(handle, win32con.WM_KEYDOWN, win32con.VK_RETURN, 0);

    #关闭所有QQ
    def closeAllQQ(self):
        os.system('taskkill /f /im QQ.exe');

    def getANewPid(self):
        rst = None;
        pids = self._collectQQ();
        for pid in pids:
            id = pid['pid'];
            if not (id in self.dictPids):
                self.dictPids[pid['pid']] = pid;
                rst = pid;
                #这里不break

        #
        return rst;

if __name__ == "__main__":
    qq = QQ();
   # qq.loginQQ();
    #qq.sendMsg("你好!","网赚");


