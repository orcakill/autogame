import threading
import time

# 共享的中断标志
interrupt_flag = False
# 共享的返回结果
fight_result = 0


def func1(name: str, num: int):
    global interrupt_flag
    global fight_result
    print("函数" + name + "开始执行")
    for i in range(num):
        if not interrupt_flag:
            if name == "1":
                print("函数" + name + "提前结束")
                interrupt_flag = True
                fight_result = name
                return True
            else:
                time.sleep(1)
    print("函数" + name + "执行结束")
    return False


def main():
    print("创建线程1")
    thread1 = threading.Thread(target=func1, args=("1", 10,))
    print("创建线程2")
    thread2 = threading.Thread(target=func1, args=("2", 20,))
    print("创建线程3")
    thread3 = threading.Thread(target=func1, args=("3", 30,))

    thread1.start()
    thread2.start()
    thread3.start()

    print("等待线程结束")
    thread1.join()
    thread2.join()
    thread3.join()
    print("主函数执行完毕")
    print(fight_result)


if __name__ == '__main__':
    main()
