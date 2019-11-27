import win32gui
import win32api


hwnd_title = dict()
def get_all_hwnd(hwnd,mouse):
    if win32gui.IsWindow(hwnd) and win32gui.IsWindowEnabled(hwnd) and win32gui.IsWindowVisible(hwnd):
        hwnd_title.update({hwnd:hwnd,hwnd:win32gui.GetWindowText(hwnd)})

def GetWindows(title):
    global hwnd_title;
    hwnd_title = dict()
    win32gui.EnumWindows(get_all_hwnd, 0);

    arr = []

    for h, t in hwnd_title.items():
        if t is not "" and t == title:
            print(h, t);
            arr.append({"hwnd":h,"title":t});

    return arr;

if __name__ == '__main__':
    GetWindows("网赚");
