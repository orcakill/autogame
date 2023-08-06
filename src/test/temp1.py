import datetime
import threading
import time

# 共享的中断标志
interrupt_flag = False


def func1():
    global interrupt_flag
    print("函数1开始执行")
    while not interrupt_flag:
        time.sleep(1)
        fun4(10)
    print("函数1执行完毕")


def func2():
    global interrupt_flag
    print("函数2开始执行")
    while not interrupt_flag:
        time.sleep(0.1)
    print("函数2执行完毕")


def func3():
    global interrupt_flag
    print("函数3开始执行")
    while not interrupt_flag:
        time.sleep(1)
    print("函数3执行完毕")


def fun4(num: int):
    time.sleep(num)
    print(num)


def main():
    thread1 = threading.Thread(target=func1)
    thread2 = threading.Thread(target=func2)
    thread3 = threading.Thread(target=func3)

    thread1.start()
    thread2.start()
    thread3.start()

    thread1.join()
    thread2.join()
    thread3.join()
    print("主函数执行完毕")


if __name__ == '__main__':
    main()
