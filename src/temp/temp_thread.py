import threading
import time


# 定义一个线程类
class MyThread(threading.Thread):
    def __init__(self, thread_id, stop_event):
        super().__init__()
        self.thread_id = thread_id
        self.stop_event = stop_event

    def run(self):
        # 线程1执行的代码
        if self.thread_id == 1:
            while not self.stop_event.is_set():
                print("Thread 1 is running...")
                time.sleep(1)
        # 线程2执行的代码
        elif self.thread_id == 2:
            while not self.stop_event.is_set():
                print("Thread 2 is running...")
                time.sleep(1)


if __name__ == '__main__':
    # 创建一个 Event 对象用于线程间通信
    stop_event = threading.Event()

    # 创建线程1和线程2，并传入共享的 Event 对象
    thread1 = MyThread(1, stop_event)
    thread2 = MyThread(2, stop_event)

    # 启动线程1和线程2
    thread1.start()
    thread2.start()

    # 模拟线程1意外中断
    # 这里使用 time.sleep 来模拟线程1中断，实际中可能是其他中断方式


    # 等待线程1和线程2结束
    thread1.join()
    thread2.join()
