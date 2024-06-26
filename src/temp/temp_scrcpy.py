import subprocess
import time, os, datetime
from PIL import Image
import win32gui, win32ui, win32api, win32con

hwnd_title = dict()  # 获取windows窗口句柄+标题


def cut_pic_by_filename_XY(filename, x1, y1, x2, y2):  # 根据图片路径，打开图片，并裁剪图片【从x1,y1到x2,y2】，然后保存裁剪出来的图片到硬盘
    img = Image.open(filename)  ## 打开filename文件，并赋值给img
    imgSize = img.size  # 大小/尺寸
    w = img.width  # 图片的宽
    h = img.height  # 图片的高
    f = img.format  # 图像格式
    region = img.crop((x1, y1, x2, y2))  # 裁剪图片【从x1,y1到x2,y2】
    current_date = datetime.datetime.now().strftime('%Y%m%d')  # 提取日期
    save_path_dir = "./image/save_image/" + current_date
    if not os.path.exists(save_path_dir):  # 文件夹不存在，则创建文件夹
        os.makedirs(save_path_dir)
    str_time = str(int(time.time()))  # 提取时间戳
    pic_filename = filename.split("/")[-1]  # 提取路径中的文件名
    region.save(save_path_dir + "/" + str_time + pic_filename)  ## 将裁剪下来的图片保存到 时间戳+文件名.png
    return save_path_dir + "/" + str_time + pic_filename  # 返回文件路径


def _get_all_hwnd(hwnd, mouse):
    if win32gui.IsWindow(hwnd) and win32gui.IsWindowEnabled(hwnd) and win32gui.IsWindowVisible(hwnd):
        hwnd_title.update({hwnd: win32gui.GetWindowText(hwnd)})


def window_capture(filename, hwnd):  # 窗口截屏
    # hwnd = 0  # 窗口的编号，0号表示当前活跃窗口
    # 根据窗口句柄获取窗口的设备上下文DC（Divice Context）
    hwndDC = win32gui.GetWindowDC(hwnd)
    # 根据窗口的DC获取mfcDC
    mfcDC = win32ui.CreateDCFromHandle(hwndDC)
    # mfcDC创建可兼容的DC
    saveDC = mfcDC.CreateCompatibleDC()
    # 创建bigmap准备保存图片
    saveBitMap = win32ui.CreateBitmap()
    # 获取监控器信息
    MoniterDev = win32api.EnumDisplayMonitors(None, None)
    w = MoniterDev[0][2][2]
    h = MoniterDev[0][2][3]
    w2 = 600  # 设置截图的X轴宽度【可根据截图保存的文件filename查看，然后实际调整】
    h2 = 1080  # 设置截图的Y轴高度【可根据截图保存的文件filename查看，然后实际调整】
    # print w,h　　　#图片大小
    # 为bitmap开辟空间
    saveBitMap.CreateCompatibleBitmap(mfcDC, w2, h2)
    # 高度saveDC，将截图保存到saveBitmap中
    saveDC.SelectObject(saveBitMap)
    # 截取从左上角（0，0）长宽为（w，h）的图片
    saveDC.BitBlt((0, 0), (w2, h2), mfcDC, (0, 0), win32con.SRCCOPY)
    saveBitMap.SaveBitmapFile(saveDC, filename)
    # 上面的截图尺寸不行，我就自己写了一个精确截图的def,其中x1,y1,x2,y2，诸君自行对比窗口截图
    backpng = cut_pic_by_filename_XY(filename, 10, 45, 590, 1070)
    return backpng

if __name__ == '__main__':
    # 可以运行以下注释的代码，获得手机的序列号,诸君可自行提取自己的手机序列号
    # cmdstr = "adb devices"
    # backstr = os.popen(cmdstr).read()
    # print(backstr)
    device_name = "8ce78c9f"
    device_n = ' -s ' + device_name
    # scrcpy --crop设定屏幕=1080*1920并且偏移坐标为 (0,0)
    # 这里的--crop命令就是老版本的-c命令，新版本升级了，-c命令是错误的了。
    # 然而：网上面的所有有关scrcpy命令的教程文档，全部还是-c命令，真鸡儿扯淡，害我查半天
    # -m 1024 限制画面分辨率=1024
    # -b 4M修改视频码率=4M
    # --window-x 100 --window-y 200 --window-width 405 --window-height 720设定窗体起始坐标，设置窗体宽和高
    win_title = "MY_Test1"
    # 注意这里是windows窗体标题，最好每次打开的windows窗体标题不同，否则多个窗体标题一样的话
    # 会出现错误，找不到句柄
    cmdstr = "scrcpy" + device_n + " --crop=1080:1920:0:0 --window-title "
    cmdstr = cmdstr + win_title
    cmdstr = cmdstr + " -m 1024 -b 4M"
    print(cmdstr)
    subprocess.Popen(cmdstr, shell=True,encoding='utf-8') # 打开scrcpy
    time.sleep(3)  # 等待3秒，等待窗体彻底弹出
    win32gui.EnumWindows(_get_all_hwnd, 0)  # 获取所有windows窗口句柄
    hwnd = 0
    for wnd in hwnd_title.items():  # 循环获取所有的windows句柄
        print(wnd)  # 句柄值示例：(325674,"MI 5")：前面是windows句柄ID，后面是windows窗口标题
        get_win_title = str(wnd[1])
        if win_title == get_win_title:  # 根据windows窗口标题判断，是不是需要截图的窗口。
            hwnd = wnd[0]
            break
    print("windows句柄ID:", hwnd)
    cut_image_file = './image/scrcpy' + str(device_name) + '.png'
    get_png = window_capture(cut_image_file, hwnd)  # 对windows窗体进行截图
    print(get_png)
    # 关闭windows窗体
    # win32gui.PostMessage(hwnd, win32con.WM_CLOSE, 0, 0)


