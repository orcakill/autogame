# @Time    : 2023年06月19日 11:57
# @Author  : orcakill
# @File    : enum.py
# @Description : 常量


class Onmyoji:
    # 游戏
    user_ACCOUNT = r"用户\首页头像"
    login_FH = r'登录\返回'
    login_SLTS = r"登录\适龄提示"
    login_YHZX = r"登录\用户中心"
    login_CY = r"登录\常用"
    home_MENU = r"首页\底部菜单栏"


class Cvstrategy:
    # 图像文字识别类型
    sift = ["sift"]


if __name__ == '__main__':
    print(Onmyoji.user_ACCOUNT)
