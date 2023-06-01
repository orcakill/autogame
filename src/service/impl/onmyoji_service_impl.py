from airtest.core.api import auto_setup
from airtest.core.helper import G

from src.service.onmyoji_service import OnmyojiService
from src.utils.my_logger import my_logger as logger


# @Time    : 2023年06月01日 08:21
# @Author  : orcakill
# @File    : onmyoji_service_impl.py
# @Description : 服务实现类
class OnmyojiServiceImpl(OnmyojiService):
    def initialization(self, user_id: str):
        logger.debug("连接Android设备")
        # 连接android设备
        auto_setup(__file__, logdir=True, devices=["android://"])
        screen1 = G.DEVICE.snapshot()
        logger.debug("截取当前页面")
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
        pass
