# @Time    : 2023年06月19日 11:57
# @Author  : orcakill
# @File    : enum.py
# @Description : 常量


class Onmyoji:
    # 游戏
    home_DBCD = r"首页\底部菜单"
    home_DBCDDK = r"首页\底部菜单打开"
    home_XZ = r"首页\下载"
    home_TS = r"首页\探索"
    login_CY = r"登录\常用"
    login_DLAN = r"登录\登录按钮"
    login_FH = r'登录\返回'
    login_FWQ = r"登录\服务器"
    login_KSYX = r"登录\开始游戏"
    login_QHFWQ = r"登录\切换服务器"
    login_QHZH = r"登录\切换账号"
    login_SLTS = r"登录\适龄提示"
    login_WYYX = r"登录\网易游戏"
    login_XSJ = r"登录\小三角"
    login_YHZX = r"登录\用户中心"
    user_XZZH = r"用户\选择账号"
    user_SYTX = r"用户\首页头像"
    comm_FH_XSFYHSCH = r"通用\返回\悬赏封印红色叉号"
    comm_FH_SYHSCH = r"通用\返回\首页红色叉号"
    comm_FH_LSYXBSXYH = r"通用\返回\蓝色圆形白色小于号"

    soul_YHTB = r"探索\御魂\御魂图标"
    soul_BQXZ = r"探索\御魂\八岐大蛇\选择八岐大蛇"
    soul_BQJC = r"探索\御魂\八岐大蛇\加成"
    soul_BQKQJC = r"探索\御魂\八岐大蛇\开启加成"
    soul_BQGBJC = r"探索\御魂\八岐大蛇\关闭加成"
    soul_HONE = r"探索\御魂\八岐大蛇\魂一"
    soul_HTEN = r"探索\御魂\八岐大蛇\魂十"
    soul_HELEVEN = r"探索\御魂\八岐大蛇\魂十一"
    soul_TZ = r"探索\御魂\八岐大蛇\挑战"
    soul_JSTX = r"探索\御魂\八岐大蛇\角色头像"
    soul_TCTZ = r"探索\御魂\八岐大蛇\退出挑战"
    soul_ZDSB = r"探索\御魂\八岐大蛇\战斗失败"
    soul_CZ = r"探索\御魂\八岐大蛇\层字"


class Cvstrategy:
    # 图像文字识别类型
    sift = ["sift"]
    default = ["mstpl", "tpl", "sift", "brisk"]


if __name__ == '__main__':
    print(Onmyoji.user_SYTX)
