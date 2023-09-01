# @Time: 2023年08月17日 09:43
# @Author: orcakill
# @File: temp_class.py
# @Description: 测试类方法自我调用
from datetime import datetime


class MyClass:
    @staticmethod
    def method1():
        print(1)

    @staticmethod
    def method2():
        MyClass.method1()  # 调用方法一
        # 方法二的实现


if __name__ == '__main__':

    # 获取当前时间
    now = datetime.now()
    # 将时间转换为字符串
    time_str = now.strftime("%Y-%m-%d %H:%M:%S")

    print(time_str)
