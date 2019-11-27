from time import sleep
import requests

import win32gui
import win32api
import win32con
import clipboard
import random;
from core.utils.util import GetWindows;

from core.utils.config import TULING123_API,TULING123_KEY,CHAT_MIN_DELTA,CHAT_MAX_DELTA
from core.utils.db import GetRndTopicMsg;

class ChatMgr:
    def __init__(self):
        self._chatWindows = [];
        self._chatWinTitle = "网赚";
        self._state = True;

        self._topic = "无聊"; #话题
        self._sender = -1;

    def setChatWinTitle(self,title):
        self._chatWinTitle = title;

    def collectChatWindows(self):
        self._chatWindows = GetWindows(self._chatWinTitle);
        if len(self._chatWindows) == 0:
            print("warnning::cant get chat window,please open the chat window!!!!!!");
        else:
            pass;

    def getRndTopic(self):
        return GetRndTopicMsg();

    def run(self):
        self.collectChatWindows();
        self._state = len(self._chatWindows) > 1;

        self._doRun();

    def doSendMsg(self, msg, hwnd):
        clipboard.copy(msg);
        if hwnd > 0:
            # win32gui.SetForegroundWindow(hwnd)  # 指定句柄设置为前台，也就是激活
            # win32gui.SetBkMode(hwnd, win32con.TRANSPARENT)# 设置为后台
            # 填充消息
            win32gui.SendMessage(hwnd, 770, 0, 0);
            # 回车发送消息
            win32gui.SendMessage(hwnd, win32con.WM_KEYDOWN, win32con.VK_RETURN, 0);

    def getMsg(self,content):
        resp = requests.post(TULING123_API, data={"key": TULING123_KEY, "info": content, })
        resp.encoding = 'utf8';
        resp = resp.json();
        return resp['text'];

    def getRndReplier(self):
        cnt = 0;
        while True:
            s = random.choice(self._chatWindows)
            if s != self._sender:
                return s;

            cnt += 1;
            if cnt > 100:
                break;

        return -1;

    def sendMsg(self,topic,sender):
        msg = self.getMsg(topic);
        self.doSendMsg(msg, sender["hwnd"]);

    def _doRun(self):
        if self._sender == -1:
            self._sender = self._chatWindows[0];

        msg = self.sendMsg(self.getRndTopic(),self._sender);

        while self._state:
            s = random.uniform(CHAT_MIN_DELTA,CHAT_MAX_DELTA);
            sleep(s);

            self._sender = self.getRndReplier();

            if self._sender != -1:
                msg = self.sendMsg(msg, self._sender);
            else:
                print("cant get the <<{0}>> chat window,please open the chat window!!!!!!",self._chatWinTitle);


    def stop(self):
        self._state = False;


if __name__ == '__main__':
    mgr = ChatMgr();
    mgr.run();





