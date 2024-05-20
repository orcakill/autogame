import time
import win32api
import win32con
import win32gui


# ---------------------------------------------------句柄配置的分割线
# 获取当前主机上的所有句柄id
def get_all_windows():
    all_window_handles = []

    # 枚举所有窗口句柄，添加到列表中
    def enum_windows_proc(hwnd, param):
        param.append(hwnd)
        return True

    # 调用枚举窗口API
    win32gui.EnumWindows(enum_windows_proc, all_window_handles)

    return all_window_handles  # 返回的是一个句柄id的列表


# 查询传入的句柄id、类名
def get_title(window_handle, class_name):
    # 查询句柄的类名
    window_class = win32gui.GetClassName(window_handle)

    # 判断窗口类名是否和指定的类名相同，如果相同则返回该窗口句柄，否则返回空值
    if window_class == class_name:
        return window_handle


# 遍历窗口句柄的所有子窗口
def get_child_windows(parent_window_handle):
    child_window_handles = []

    def enum_windows_proc(hwnd, param):
        param.append(hwnd)
        return True

    # win32gui.EnumChildWindows    遍历窗口句柄的所有子窗口
    win32gui.EnumChildWindows(parent_window_handle, enum_windows_proc, child_window_handles)
    return child_window_handles


# 根据标题查找窗口句柄
def find_hwnd_by_title(title):
    all_windows = get_all_windows()  # 查询所有句柄
    matched_windows = []  # 存放所有匹配类名的句柄id

    # 在所有窗口中查找标题匹配的窗口句柄
    for window_handle in all_windows:
        # get_title方法  检查传入句柄对应的类名和我们实际的类名是否对应
        window_title = get_title(window_handle, title)
        if window_title:
            matched_windows.append(window_title)  # 如果对应就写入列表

    # 如果没有匹配到，则在所有子窗口中查找标题匹配的窗口句柄
    if matched_windows:
        return matched_windows
    else:
        child_window_handles = []
        for parent_window_handle in all_windows:
            # 不论子窗口是否有数据都追加到列表
            child_window_handles.extend(get_child_windows(parent_window_handle))
        for child_window_handle in child_window_handles:
            if get_title(child_window_handle, title):
                matched_windows.append(get_title(child_window_handle, title))
    return matched_windows


# -----------------------------------------------------句柄配置的分割线


def getPointOnLine(start_x, start_y, end_x, end_y, ratio):
    x = ((end_x - start_x) * ratio) + start_x
    y = ((end_y - start_y) * ratio) + start_y
    return int(round(x)), int(round(y))


# 声明鼠标操作的类
class WinMouse(object):

    # 初始化函数，接受传入的句柄id
    def __init__(self, handle_num: int, num_of_steps=80):
        self.handle = handle_num
        self.num_of_steps = num_of_steps

        # 鼠标左键按下

    def left_button_down(self, pos):
        win32api.PostMessage(self.handle, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, pos)

    # 鼠标左键释放
    def left_button_up(self, pos):
        win32api.PostMessage(self.handle, win32con.WM_LBUTTONUP, None, pos)

    # 按下鼠标左键并移动
    def mouse_move(self, pos):
        win32api.PostMessage(self.handle, win32con.WM_MOUSEMOVE, win32con.MK_LBUTTON, pos)

    # 按下鼠标右键并移动
    def right_button_move(self, pos):
        win32api.PostMessage(self.handle, win32con.WM_MOUSEMOVE, win32con.MK_RBUTTON, pos)

    # 指定坐标按下右键
    def right_button_down(self, pos):
        win32api.PostMessage(self.handle, win32con.WM_RBUTTONDOWN, win32con.MK_RBUTTON, pos)

    # 右键释放
    def right_button_up(self, pos):
        win32api.PostMessage(self.handle, win32con.WM_RBUTTONUP, None, pos)

    # --------------------------------------------------------封装按键方法的分割线

    # 让他可以直接接收x，y坐标，wait是松开按键的间隔，一般默认即可
    # 左键单击
    def left_click(self, x_pos: int, y_pos: int, wait=0.2):
        point = win32api.MAKELONG(x_pos, y_pos)
        self.left_button_down(point)
        time.sleep(wait)
        self.left_button_up(point)

    # 右键单击
    def right_click(self, x_pos: int, y_pos: int, wait=0.2):
        point = win32api.MAKELONG(x_pos, y_pos)
        self.right_button_down(point)
        time.sleep(wait)
        self.right_button_up(point)

    # 模拟左键双击
    def left_double_click(self, x_pos: int, y_pos: int, click=2, wait=0.4):
        wait = wait / click  # click 表示点击次数，wait是的等待时间，意思是双击的间隔
        point = win32api.MAKELONG(x_pos, y_pos)
        for i in range(click):
            self.left_button_down(point)
            time.sleep(wait)
            self.left_button_up(point)

    # 右键双击
    def right_doubleClick(self, x, y, click=2, wait=0.4):
        wait = wait / click
        pos = win32api.MAKELONG(x, y)
        for i in range(click):
            self.right_button_down(pos)
            time.sleep(wait)
            self.right_button_up(pos)

    # 模拟点击并拖拽目标，接受两对坐标值
    # 模拟点击并拖拽目标，接受两对坐标值
    def left_click_move(self, x1: int, y1: int, x2: int, y2: int, wait=2):
        point1 = win32api.MAKELONG(x1, y1)
        self.left_button_down(point1)  # 起始点按下鼠标左键
        # 获取我们在init初始化时定义的偏移值
        steps = self.num_of_steps

        # 调用我们上面的方法返回具体，循环0-80的值
        # 你看这里的循环值是80，也就说会做80次循环操作
        # 我们传入了起始坐标和目标坐标，而i / steps就相当于起始到结束的偏移位置
        # 可以理解为从左上角到右下角的点
        points = [getPointOnLine(x1, y1, x2, y2, i / steps) for i in range(steps)]
        points.append((x2, y2))
        wait_time = wait / steps
        unique_points = list(set(points))
        unique_points.sort(key=points.index)
        for point in unique_points:
            x, y = point
            point = win32api.MAKELONG(x, y)
            self.mouse_move(point)
            time.sleep(wait_time)
        self.left_button_up(point)

    # 右键单击并滑动批量勾选（与上方函数同理）
    def right_click_move(self, start_x, start_y, end_x, end_y, wait=2):
        pos = win32api.MAKELONG(start_x, start_y)
        self.right_button_down(pos)
        steps = self.num_of_steps
        points = [getPointOnLine(start_x, start_y, end_x, end_y, i / steps) for i in range(steps)]
        points.append((end_x, end_y))
        time_per_step = wait / steps
        distinct_points = list(set(points))
        distinct_points.sort(key=points.index)
        for point in distinct_points:
            x, y = point
            pos = win32api.MAKELONG(x, y)
            self.right_button_move(pos)
            time.sleep(time_per_step)
        self.right_button_up(pos)


if __name__ == '__main__':
    hwnd = find_hwnd_by_title("Edit")  # 通过类名获取句柄
    bd = WinMouse(hwnd[0])  # 实例化WinMouse 类,传入句柄值

    bd.left_click_move(109, 180, 232, 341)