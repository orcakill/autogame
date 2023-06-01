# python中没有接口，只能自己实现


class Interface:
    def func1(self):
        pass

    def func2(self):
        pass


class Test(Interface):
    def func1(self):
        print('重写了func1')

    def func2(self):
        print('重写了func2')

    def func3(self):
        print('新加入了func3')


if __name__ == '__main__':
    a = Test()
    a.func1()
    a.func2()
    a.func3()