# @Time    : 2023年06月30日 11:56
# @Author  : orcakill
# @File    : kwarg_test.py
# @Description : TODO

def cs_test1(s:str):
    t=(1,2)
    if s=="1":
        return True
    else:
        return t[0]



if __name__ == '__main__':
    print(cs_test1("1"))
    print(cs_test1("2"))
