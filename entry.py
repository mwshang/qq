
from core.qq.qqmgr import QQMgr;

if __name__ == "__main__":
    mgr = QQMgr();

    s = input("1.Login and Chat     \t\n2.Chat  \nPlease select:");
    if s == "2":
        mgr.runChat();
    else:
        mgr.run();