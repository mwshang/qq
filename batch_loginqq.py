#coding=utf-8
_author_="pholy"

import os
import win32gui
import win32api
import win32con
from pykeyboard import PyKeyboard
import time
from ctypes import *
import sqlite3

#######################################################################################
#QQ登录，参数为qq号码和密码，QQ的安装路径为C盘。
#######################################################################################
def qq_login(qq,pwd):
    os.system('"C:\Program Files (x86)\Tencent\QQ\Bin\QQScLauncher.exe"')
    time.sleep(3)
    a=win32gui.FindWindow(None,"QQ")#获取窗口的句柄，参数1：类名，参数2：标题
    loginid=win32gui.GetWindowPlacement(a)
    windll.user32.SetCursorPos(loginid[4][0]+211,loginid[4][1]+247)#置鼠标的位置
    # print(loginid)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,0,0,0,0)#按下鼠标左键
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,0,0,0,0)#松开鼠标左键
    time.sleep(3)
    k=PyKeyboard()
    k.type_string(qq)#输入QQ号码
    time.sleep(3)
    win32api.keybd_event(9,0,0,0)#按下Tab键
    win32api.keybd_event(9,0,win32con.KEYEVENTF_KEYUP,0)#松开Tab键
    time.sleep(3)
    k.type_string(pwd)#输入QQ密码
    # print(pwd)
    time.sleep(3)
    win32api.keybd_event(13,0,0,0)#按下Enter键
    win32api.keybd_event(13,0,win32con.KEYEVENTF_KEYUP,0)#松开Enter键
    qstr = 3 * "*" + qq[3:]
    print('{}登录成功'.format(qstr))
    time.sleep(6)

#######################################################################################
#txt文件模式登录。每行一个QQ号信息（12345678---qwert123456）,中间用三个短横线隔开
#######################################################################################
def TxtLogin(path):
    # fn="D:\myInfo\qq.txt"
    fr=open(path,'r').readlines()
    # print(fr)
    for i in fr:
        info=i.split('---')
        # print(info[1])
        qq_login(str(info[0]),str(info[1]))

#######################################################################################
#sqlite3数据库模式登录。表结构有三个字段（id,qq,pwd）
#######################################################################################
def DbLogin(path):
    conn=sqlite3.connect(path)
    c=conn.cursor()
    cursor=c.execute("select * from qq")
    for row in cursor:
        qq_login(str(row[1]),str(row[2]))
        print('{}----{}'.format(row[1],row[2]))
        print(row[2])
    conn.close()

DB_PATH="D:\QQ.db"
TXT_PATH="D:\qq.txt"
#######################################################################################
#登录方式二选一，关闭电脑管家进行登录，不然会出现用户名和密码错误，搞不懂是什么鬼，
# 卸了最好！
#######################################################################################
# DbLogin(DB_PATH)
TxtLogin(TXT_PATH)
