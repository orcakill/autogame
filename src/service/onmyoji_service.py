from src.service.airtest_service import AirtestService
from src.utils.junk.my_logging import logger

# @Time    : 2023年05月31日 17:51
# @Author  : orcakill
# @File    : onmyoji_service.py
# @Description : 服务接口

airtest_service = AirtestService()


class OnmyojiService:
    @staticmethod
    def initialization(user_id: str):
        logger.debug("连接Android设备")
        # 连接android设备
        airtest_service.auto_setup()
        logger.info("截取当前页面")
        airtest_service.snapshot()
        # 在auto_setup接口传入devices参数
        # start_app("com.netease.onmyoji")
        # 判断当前是否是用户首页
        # 当前不是用户首页，重启app
        # 切换账号
        # 选择服务器
        # 进入游戏
        # 判断是否是用户首页
        # 处理异常页面，如购买、加成取消
        # 打开底部菜单栏
        # 初始化结束，进程ID、项目组ID、项目ID、项目执行时间、项目完成情况
