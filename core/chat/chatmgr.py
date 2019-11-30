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
from core.utils.log import log;


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
            log("warnning::cant get chat window,please open the chat window!!!!!!");
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
            log("{0} say:{1}".format(hwnd,msg))
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

        if len(self._chatWindows) == 0:
            return -1;

        cnt = 0;
        while True:
            s = random.choice(self._chatWindows)
            if s != self._sender:
                return s;

            cnt += 1;
            if cnt > 100:
                break;

        return -1;

    def sendMsg(self,topic,sender,isGetReply=True):
        if isGetReply:
            msg = self.getMsg(topic);
        else:
            msg = topic;
        self.doSendMsg(msg, sender["hwnd"]);

    def _doRun(self):

        while len(self._chatWindows) == 0:
            log("Please open the {0} chat window to continue!".format(self._chatWinTitle));
            sleep(5);
            self.collectChatWindows();

        self._state = True;
        if self._sender == -1:
            self._sender = self._chatWindows[0];

        refreshCount = 0;
        chgTopicCount = 0;
        log("start to chat!!!!!");
        msg = self.sendMsg(self.getRndTopic(),self._sender,False);

        while self._state:
            s = random.uniform(CHAT_MIN_DELTA,CHAT_MAX_DELTA);
            sleep(s);

            self._sender = self.getRndReplier();

            if self._sender != -1:
                chgTopicCount += 1;
                if chgTopicCount > 5:
                    chgTopicCount = 0;
                    msg = self.getRndTopic();
                    log("change topic:{0}".format(msg));
                    msg = self.sendMsg(msg, self._sender,False);
                else:
                    msg = self.sendMsg(msg, self._sender);
            else:
                log("cant get the <<{0}>> chat window,please open the chat window!!!!!!".format(self._chatWinTitle));
                self.collectChatWindows();
                refreshCount = 0;

            refreshCount += 1;
            if refreshCount > 5 :
                refreshCount = 0;
                self.collectChatWindows();



    def stop(self):
        self._state = False;


if __name__ == '__main__':
    mgr = ChatMgr();
    mgr.run();





