import time
import win32api
import win32gui


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


if __name__ == '__main__':
    hwnd = find_hwnd_by_title("Edit")
    print(hwnd)