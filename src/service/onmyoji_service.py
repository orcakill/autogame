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
        account_index=os.path.join(Onmyoji.login_ACCOUNT,user_id)
        is_index = image_service.exists(account_index)
        if is_index:
            logger.debug("账号首页")
        else:
            logger.debug("其它情况")
        # 不在账号首页的其它，重启app，根据账号选择用户、服务器、开始游戏
        logger.debug("初始化当前状态完成")
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
