# @Time    : 2023年06月19日 11:57
# @Author  : orcakill
# @File    : enum.py
# @Description : 常量


class Onmyoji:
    # 游戏
    user_ACCOUNT = r"用户\首页头像"
    user_XZZH= r"用户\选择账号"
    login_FH = r'登录\返回'
    login_SLTS = r"登录\适龄提示"
    login_YHZX = r"登录\用户中心"
    login_CY = r"登录\常用"
    login_DLAN = r"登录\登录按钮"
    login_QHFWQ = r"登录\切换服务器"
    login_XSJ = r"登录\小三角"
    login_FWQ = r"登录\服务器"
    login_KSYX = r"登录\开始游戏"
    login_QHZH = r"登录\切换账号"
    login_WYYX = r"登录\网易游戏"
    home_DBCD = r"首页\底部菜单栏"
    home_DBCDDK = r"首页\底部菜单栏打开"
    home_FH = r"首页\返回"
    home_XZ = r"首页\下载"


class Cvstrategy:
    # 图像文字识别类型
    sift = ["sift"]
    default=["mstpl", "tpl", "sift", "brisk"]


if __name__ == '__main__':
    print(Onmyoji.user_ACCOUNT)
