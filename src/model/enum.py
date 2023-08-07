# @Time: 2023年06月19日 11:57
# @Author: orcakill
# @File: enum.py
# @Description: 常量


class Onmyoji:
    # 结界突破
    border_GRJJ = r"探索\结界突破\个人结界"
    border_SX = r"探索\结界突破\刷新"
    border_SXQD = r"探索\结界突破\刷新确定"
    border_JJSY = r"探索\结界突破\结界首页"
    border_YSJTP = r"探索\结界突破\右上角突破"
    border_GRJJWSB = r"探索\结界突破\个人结界无失败"
    border_ZB = r"探索\结界突破\准备"
    border_GTRQ = r"探索\结界突破\呱太入侵"
    border_ZDSB = r"探索\结界突破\战斗失败"
    border_ZDSL = r"探索\结界突破\战斗胜利"
    border_ZBBZ = r"探索\结界突破\战败标志"
    border_WJJTZJ = r"探索\结界突破\无结界挑战劵"
    border_JJTZJWP = r"探索\结界突破\结界挑战劵误判"
    border_JJTPTB = r"探索\结界突破\结界突破图标"
    border_JSTXDH = r"探索\结界突破\角色头像大号"
    border_JSTXXH = r"探索\结界突破\角色头像小号"
    border_JG = r"探索\结界突破\进攻"
    border_XH = r"探索\结界突破\消耗"
    border_TCTZ = r"探索\结界突破\退出挑战"
    border_ZCTZ = r"探索\结界突破\再次挑战"
    border_SDZR = r"探索\结界突破\锁定阵容"
    # 返回
    comm_FH_LSYXBSXYH = r"通用\返回\蓝色圆形白色小于号"
    comm_FH_SYHDBSCH = r"通用\返回\首页红底白色叉号"
    comm_FH_XSFYHSCH = r"通用\返回\悬赏封印红色叉号"
    comm_FH_YSJZDHBSCH = r"通用\返回\右上角棕底红白色叉号"
    # 首页
    home_DBCD = r"首页\底部菜单"
    home_DBCDDK = r"首页\底部菜单打开"
    home_TS = r"首页\探索"
    home_XZ = r"首页\下载"
    home_QX = r"首页\取消"
    # 登录
    login_CY = r"登录\常用"
    login_DLAN = r"登录\登录按钮"
    login_FWQ = r"登录\服务器"
    login_KSYX = r"登录\开始游戏"
    login_QHFWQ = r"登录\切换服务器"
    login_QHZH = r"登录\切换账号"
    login_SLTS = r"登录\适龄提示"
    login_WYYX = r"登录\网易游戏"
    login_XSJ = r"登录\小三角"
    login_TYCS = r"登录\特邀测试"
    login_ZXJS = r"登录\注销角色"
    login_YHZX = r"登录\用户中心"
    # 御魂
    soul_BQGBJC = r"探索\御魂\八岐大蛇\关闭加成"
    soul_BQJC = r"探索\御魂\八岐大蛇\加成"
    soul_BQKQJC = r"探索\御魂\八岐大蛇\开启加成"
    soul_BQXZ = r"探索\御魂\八岐大蛇\选择八岐大蛇"
    soul_CZ = r"探索\御魂\八岐大蛇\层字"
    soul_HELEVEN = r"探索\御魂\八岐大蛇\魂十一"
    soul_HONE = r"探索\御魂\八岐大蛇\魂一"
    soul_HTEN = r"探索\御魂\八岐大蛇\魂十"
    soul_JSTXDH = r"探索\御魂\八岐大蛇\角色头像大号"
    soul_JSTXXH = r"探索\御魂\八岐大蛇\角色头像小号"
    soul_JSTXDS = r"探索\御魂\八岐大蛇\角色头像打手"
    soul_ZD = r"探索\御魂\八岐大蛇\自动"
    soul_TCTZ = r"探索\御魂\八岐大蛇\退出挑战"
    soul_TZ = r"探索\御魂\八岐大蛇\挑战"
    soul_WS = r"探索\御魂\八岐大蛇\喂食"
    soul_WSXSJ = r"探索\御魂\八岐大蛇\喂食小三角"
    soul_YHTB = r"探索\御魂\御魂图标"
    soul_ZDSB = r"探索\御魂\八岐大蛇\战斗失败"
    # 用户
    user_SYTX = r"用户\首页头像"
    user_XZZH = r"用户\选择账号"


class Cvstrategy:
    # 图像文字识别类型
    sift = ["sift"]
    default = ["mstpl", "tpl", "sift", "brisk"]


if __name__ == '__main__':
    print(Onmyoji.user_SYTX)
