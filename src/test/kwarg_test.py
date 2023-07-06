# @Time    : 2023年06月30日 11:56
# @Author  : orcakill
# @File    : kwarg_test.py
# @Description : TODO

def cs_test1():
    for i in range(1, 6):
        print("第一层" + str(i))
        for i in range(1, 4):
            print("第二层" + str(i))


if __name__ == '__main__':
    cs_test1()
