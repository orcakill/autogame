# @Time: 2023年08月17日 09:43
# @Author: orcakill
# @File: temp_class.py
# @Description: 测试类方法自我调用
class MyClass:
    @staticmethod
    def method1():
        print(1)

    @staticmethod
    def method2():
        MyClass.method1()  # 调用方法一
        # 方法二的实现


if __name__ == '__main__':
    for i in range(1,9):
        print(i)
    MyClass.method2()
