# @Time    : 2023年05月31日 17:51
# @Author  : orcakill
# @File    : onmyoji_service.py
# @Description : 服务接口
import os

from src.service.airtest_service import AirtestService
from src.service.image_service import ImageService
from src.utils.junk.my_logging import logger
from src.model.enum import Onmyoji

# airtest服务接口
airtest_service = AirtestService()
image_service = ImageService()


class OnmyojiService:
    @staticmethod
    def initialization(user_id: str):
        logger.debug("判断当前状态")
        # 当前状态 账号首页 1，2,3，4
        #        其它，不在账号首页
        account_index = os.path.join(Onmyoji.login_ACCOUNT, user_id)
        is_index = image_service.exists(account_index)
        if is_index:
            logger.debug("账号首页")
        else:
            # 不在账号首页的其它，重启app，根据账号选择用户、服务器、开始游戏
            logger.debug("其它情况，重启app")
            airtest_service.restart_app("")
            logger.debug("等待20秒")
            logger.debug("点击左上角，防止有开场动画")
            logger.debug("判断是否存在适龄提示、返回按钮")
            logger.debug("确定当前页面适龄提示+开始游戏")
            logger.debug("登录账号")
            logger.debug("用户中心")
            logger.debug("切换账号")
            logger.debug("选择服务器")
            logger.debug("开始游戏")
            logger.debug("当前是否是账号首页")
        logger.debug("菜单栏是否已打开")
        logger.debug("初始化当前状态完成")
