# @Time    : 2023年05月31日 17:51
# @Author  : orcakill
# @File    : onmyoji_service.py
# @Description : 服务接口
import os
import time

from src.model.models import GameAccount
from src.service.airtest_service import AirtestService
from src.service.image_service import ImageService
from src.utils.junk.my_logging import logger
from src.model.enum import Onmyoji, Cvstrategy

# airtest服务接口
airtest_service = AirtestService()
image_service = ImageService()


class OnmyojiService:
    @staticmethod
    def initialization(game_account: GameAccount):
        # 判断是否是待登录账号首页
        logger.debug("判断当前状态")
        # 当前状态 账号首页 1，2,3，4
        #        其它，不在账号首页
        account_index = os.path.join(Onmyoji.user_SYTX, game_account.id)
        is_index = image_service.exists(account_index)
        if not is_index:
            logger.debug("不在账号首页")
            # 不在账号首页的其它，重启app，根据账号选择用户、服务器、开始游戏
            logger.debug("启动阴阳师app")
            airtest_service.restart_app("com.netease.onmyoji")
            logger.debug("等待20秒")
            time.sleep(20)
            logger.debug("判断是否存在适龄提示")
            is_ageAppropriateReminder = image_service.exists(Onmyoji.login_SLTS, timeout=5)
            # 不存在适龄提示
            if not is_ageAppropriateReminder:
                logger.debug("不存在适龄提示")
                for i_ageAppropriateReminder in range(5):
                    logger.debug("点击左上角，防止有开场动画")
                    airtest_service.touch_coordinate([10, 10])
                    logger.debug("点击公告返回")
                    image_service.touch(Onmyoji.login_FH)
                    logger.debug("重新判断适龄提示")
                    is_ageAppropriateReminder = image_service.exists(Onmyoji.login_SLTS)
                    if is_ageAppropriateReminder:
                        break
                    logger.debug("等待10秒")
                    time.sleep(10)
            logger.debug("登录账号")
            logger.debug("判断当前账号选择")
            is_account_select = image_service.exists(Onmyoji.login_WYYX)
            if not is_account_select:
                logger.debug("用户中心")
                image_service.touch(Onmyoji.login_YHZX)
                logger.debug("切换账号")
                image_service.touch(Onmyoji.login_QHZH)
            logger.debug("常用")
            image_service.touch(Onmyoji.login_CY)
            logger.debug("选择账号")
            account = os.path.join(Onmyoji.user_XZZH, game_account.id)
            image_service.touch(account)
            logger.debug("登录")
            image_service.touch(Onmyoji.login_DLAN)
            logger.debug("切换服务器")
            image_service.touch(Onmyoji.login_QHFWQ,cvstrategy=Cvstrategy.default)
            logger.debug("点击小三角")
            image_service.touch(Onmyoji.login_XSJ, cvstrategy=Cvstrategy.default)
            logger.debug("选择服务器:{}", game_account.game_region)
            server = os.path.join(Onmyoji.login_FWQ, game_account.game_region)
            image_service.touch(server)
            logger.debug("开始游戏")
            image_service.touch(Onmyoji.login_KSYX)
            time.sleep(15)
        logger.debug("当前账号首页,判断底部菜单")
        is_openBottom = image_service.exists(Onmyoji.home_DBCDDK)
        if not is_openBottom:
            for i_openBottom in range(4):
                logger.debug("当前页面无底部菜单打开")
                logger.debug("点击可能存在的右上角返回")
                image_service.touch(Onmyoji.comm_SYHSCH, timeout=3)
                logger.debug("点击可能存在的下载")
                image_service.touch(Onmyoji.home_XZ, timeout=3)
                logger.debug("点击可能存在的底部菜单")
                image_service.touch(Onmyoji.home_DBCD, timeout=3)
                logger.debug("重新判断是否存在底部菜单打开")
                is_openBottom = image_service.exists(Onmyoji.home_DBCDDK)
                if is_openBottom:
                    break
        logger.info("初始化当前状态完成")
