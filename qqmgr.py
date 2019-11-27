#coding=utf-8
import os;
import time;

import win32gui
import win32api
import win32con
import pymouse
import psutil
import clipboard
import threading
import sched;
from pymouse import *
from pykeyboard import PyKeyboard
from ctypes import *

#----------------------------config--------------------------
QQ_LIST = "qq.txt";
QQ_PATH = '"D:\Program Files (x86)\Tencent\QQ\Bin\QQScLauncher.exe"';

# 批次执行最大间隔
BATCH_MAX_DELTA = 10;
# 执行最大次数,如果需要无限循环,可以调到最大
BATCH_MAX_COUNT = 2;

#==============================================================

#生成调度器
scheduler = sched.scheduler(time.time, time.sleep)

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
        handle = win32gui.FindWindow(None,targetName)
        if handle > 0 :
            # 填充消息
            win32gui.SendMessage(handle, 770, 0, 0);
            # 回车发送消息
            win32gui.SendMessage(handle, win32con.WM_KEYDOWN, win32con.VK_RETURN, 0);

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

class QQMgr:
    def __init__(self):
        self.qqList = [];
        self.dictPids = {}
        self.qqPidName = "QQ.exe";

        self.loginCount = 3;#每次登陆的数量
        self.loginIndex = 0;
        self.executedCount = 0;

        self._initData();

    def _initData(self):

        #------------------------------------
        F = open(QQ_LIST, "r").readlines()
        for i in F:
            tx = i.split('----')
            # print (tx[0])#打印用户名
            # print (tx[1])#打印密码
            qq = QQ({"qq": tx[0], "pwd": tx[1]},self);
            self.qqList.append(qq);
        #=========================================

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

    def doLogin(self):
        total = len(self.qqList)

        if self.loginIndex < total and self.executedCount < BATCH_MAX_COUNT:
            endIndex = min(self.loginIndex + self.loginCount,total);
            tmpCnt = 0
            for i in range(self.loginIndex,endIndex):
                tmpCnt += 1;
                self._doLogin(i);

            self.loginIndex = endIndex;

            if tmpCnt < self.loginCount and self.executedCount < BATCH_MAX_COUNT - 1:
                self.executedCount += 1;
                self.loginIndex = 0
                endIndex = self.loginCount - tmpCnt;
                for i in range(self.loginIndex, endIndex):
                    self._doLogin(i);

                self.loginIndex = endIndex;

            if self.loginIndex == total:
                self.executedCount += 1;
                if self.executedCount < BATCH_MAX_COUNT:
                    self.loginIndex = 0;
                    return False;
                return True;
            elif self.executedCount >= BATCH_MAX_COUNT:
                return True;
            return False;
        return True;

    def _doLogin(self,index):
        qq = self.qqList[index];
        print("Start to login qq:" + qq.getQQNum());
        while not qq.isLogined() and qq.loginQQ():
            time.sleep(3);
            # qq.setPInfo(self.getANewPid());
            print("Finished to login qq:{0} pid:{1}".format(qq.getQQNum(), qq.getPId()));
            break;

    def _doRun(self):
        # 先关闭已登陆的QQ
        self.closeLoginedQQ();

        flag = self.doLogin();

        if flag == False:
            scheduler.enter(BATCH_MAX_DELTA,1,self._doRun);

    def run(self):
        self._doRun();
        scheduler.run();

    def getANewPid(self):
        # 注意,QQ登陆的时候可能会有多个进程,所以使用数组
        rst = [];
        pids = self._collectQQ();
        for pid in pids:
            id = pid['pid'];
            if not (id in self.dictPids):
                self.dictPids[pid['pid']] = pid;
                rst.append(pid);

        return rst;

    # 关闭已登陆的QQ
    def closeLoginedQQ(self):
        for qq in self.qqList:
            if qq.isLogined():
                self.closeQQ(qq);

        #os.system('taskkill /f /im QQ.exe');

    def closeQQ(self,qq):
        self.dictPids[qq.getPId()] = None;
        qq.close();


if __name__ == "__main__":
    mgr = QQMgr();
    mgr.run();

    #qq.sendMsg("你好!","网赚");