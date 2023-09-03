"""
# @Time: 2023年09月02日23:09
# @Author: orcakill
# @File: temp_thread2.py
# @Description: 线程测试 thread
"""

import threading
import time

# 共享变量，用于控制子线程2的执行状态
exit_flag = False


# 子线程1的函数
def thread1_func():
    global exit_flag
    print("子线程1开始")
    time.sleep(10)
    print("子线程1结束")
    exit_flag = True


# 子线程2的函数
def thread2_func():
    while not exit_flag:
        time.sleep(1)
        print("子线程2运行中...")

    print("子线程2结束")


if __name__ == '__main__':
    # 创建子线程1和子线程2
    thread1 = threading.Thread(target=thread1_func)
    thread2 = threading.Thread(target=thread2_func)

    try:
        # 启动子线程1和子线程2
        thread1.start()
        thread2.start()

        # 等待子线程1结束
        thread1.join()

        # 等待子线程2结束
        thread2.join()
    except KeyboardInterrupt:
        # 捕获键盘中断信号，结束子线程1和子线程2
        print("主线程异常中断，结束子线程1和子线程2")
        exit_flag = True

    print("主线程结束")
