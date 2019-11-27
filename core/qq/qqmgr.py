#coding=utf-8
import time;
import psutil
import sched;

from core.qq.qq import QQ;
from core.chat.chatmgr import ChatMgr;
from core.utils.config import QQ_LIST,BATCH_MAX_COUNT,BATCH_MAX_DELTA;

#生成调度器
scheduler = sched.scheduler(time.time, time.sleep)

class QQMgr:
    def __init__(self):
        self.qqList = [];
        self.dictPids = {}
        self.qqPidName = "QQ.exe";

        self.chatWinTitle = "网赚";

        self.loginCount = 3;#每次登陆的数量
        self.loginIndex = 0;
        self.executedCount = 0;

        self.chatMgr = ChatMgr();

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
        self.chatMgr.stop();

        flag = self.doLogin();

        self.chatMgr.setChatWinTitle(self.chatWinTitle);
        print("please open the {0} chat window,after 12s to run autochat!!!!! ".format(self.chatWinTitle));
        time.sleep(12);
        self.chatMgr.run();
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