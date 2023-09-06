import threading
import time

# 共享变量，用于控制子线程2的执行状态
exit_flag = False


def thread_func():
    print("函数正常开始")
    global exit_flag
    # 创建子线程1和子线程2
    thread1 = threading.Thread(target=thread1_func)
    thread2 = threading.Thread(target=thread2_func)
    # 启动子线程1和子线程2
    thread1.start()
    thread2.start()

    try:
        # 等待子线程1结束
        thread1.join()
        # 等待子线程2结束
        thread2.join()
        print("函数正常结束")
    except KeyboardInterrupt:
        exit_flag = True
        thread1.join()
        thread2.join()
        print("函数异常中断，结束子线程1和子线程2")


# 子线程1的函数
def thread1_func():
    global exit_flag
    try:
        print("子线程1开始")
        time.sleep(10)
        print("子线程1运行中..." + str(exit_flag))
        print("子线程1正常结束")
        exit_flag = True
    except KeyboardInterrupt:
        print("子线程异常中断")



# 子线程2的函数
def thread2_func():
    global exit_flag
    while not exit_flag:
        try:
            time.sleep(1)
            print("子线程2运行中..." + str(exit_flag))
        except KeyboardInterrupt:
            exit_flag = True
            print("子线程2异常中断")
    print("子线程2正常结束")


if __name__ == '__main__':
    print("主函数正常开始")
    thread_func()
    print("主函数正常结束")
