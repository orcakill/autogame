import datetime
import threading
import time

# 共享的中断标志
interrupt_flag = False


def func1(num:int):
    global interrupt_flag
    print("函数1开始执行")
    for i in range(num):
        if not interrupt_flag:
            time.sleep(1)
    print("函数1执行完毕")
    interrupt_flag=True


def func2(num:int):
    global interrupt_flag
    print("函数2开始执行")
    for i in range(num):
        if not interrupt_flag:
            time.sleep(1)
    print("函数2执行完毕")


def func3(num:int):
    global interrupt_flag
    print("函数3开始执行")
    for i in range(num):
        if not interrupt_flag:
            time.sleep(1)
    print("函数3执行完毕")


def main():
    print("创建线程1")
    thread1 = threading.Thread(target=func1, args=(10,))
    print("创建线程2")
    thread2 = threading.Thread(target=func2, args=(20,))
    print("创建线程3")
    thread3 = threading.Thread(target=func3, args=(30,))

    thread1.start()
    thread2.start()
    thread3.start()

    print("等待线程结束")
    thread1.join()
    thread2.join()
    thread3.join()
    print("主函数执行完毕")


if __name__ == '__main__':
    main()
