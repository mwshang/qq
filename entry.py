
from core.qq.qqmgr import QQMgr;

if __name__ == "__main__":
    mgr = QQMgr();
    name = input("请输入群聊名称:")
    if name != "":
        mgr.setChatWinTitle(name);

    s = input("1.登陆,聊天     \t\n2.聊天  \n请选择:");
    if s == "2":
        mgr.runChat();
    else:
        mgr.run();