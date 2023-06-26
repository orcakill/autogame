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
from src.model.enum import Onmyoji

# airtest服务接口
airtest_service = AirtestService()
image_service = ImageService()


class OnmyojiService:
    @staticmethod
    def initialization(game_account: GameAccount):
        logger.debug("判断当前状态")
        # 当前状态 账号首页 1，2,3，4
        #        其它，不在账号首页
        account_index = os.path.join(Onmyoji.user_ACCOUNT, game_account.id)
        is_index = image_service.exists(account_index)
        if is_index:
            logger.debug("账号首页")
            # 判断当前是否是否打开底部菜单栏
            is_menu = image_service.exists(Onmyoji.home_MENU)
            if not is_menu:
                logger.debug("未打开底部菜单")
                image_service.touch(Onmyoji.home_MENU)
            else:
                logger.debug("底部菜单已打开")
        else:
            # 不在账号首页的其它，重启app，根据账号选择用户、服务器、开始游戏
            logger.debug("其它情况，重启阴阳师app")
            airtest_service.restart_app("com.netease.onmyoji")
            logger.debug("等待20秒")
            time.sleep(20)
            logger.debug("点击左上角，防止有开场动画")
            airtest_service.touch_coordinate([10, 10])
            logger.debug("判断是否存在适龄提示")
            is_ageAppropriateReminder = image_service.exists(Onmyoji.login_SLTS)
            if not is_ageAppropriateReminder:
                logger.debug("无适龄提示，点击公告返回")
                image_service.touch(Onmyoji.login_FH)
            logger.debug("登录账号")
            logger.debug("用户中心")
            image_service.touch(Onmyoji.login_YHZX)
            logger.debug("常用")
            image_service.touch(Onmyoji.login_CY)
            logger.debug("选择账号")
            # if  game_account.account_name==1:
            #     logger.debug("手机号178")
            #     imagesBack (login_XZZH_PHONE1, paramSIFT (process, 0.8, 4))
            #
            # if (gameUserId.equals ("2")) {
            # logger.debug("邮箱号1")
            # imagesBack (login_YHZX_EMAIIL1, paramSIFT (process, 0.8, 4))
            # }
            # logger.debug("登录")
            # imagesBack(login_DL, paramSIFT(process))
            # logger.debug("切换服务器")
            # imagesBack(login_QH, paramSIFT(process))
            # logger.debuginfo("点击小三角")
            # imagesBack(login_XSJ, paramSIFT(process, 0.8, 4))
            # if (gameUserId != null) {
            # if (gameUserId.equals ("1")) {
            # logger.debug("点击大号角色-缥缈之旅")
            # imagesBack (login_FWQ_PMZL, paramSIFT (process))
            # }
            # if (gameUserId.equals ("2")) {
            # logger.debug ("点击小号角色1-缥缈之旅")
            # imagesBack (login_FWQ_PMZL, paramSIFT (process))
            # }
            # if (gameUserId.equals ("3")) {
            # logger.debug ("点击小号角色2-两情相悦")
            # imagesBack (login_FWQ_LQXY, paramSIFT (process))
            # }
            # if (gameUserId.equals ("4")) {
            # logger.debug ("点击小号角色2-桃映春馨")
            # imagesBack (login_FWQ_TYCX, paramSIFT (process))
            # }
            # }
            # logger.debug("开始游戏")
            # imagesBack(login_KSYX, paramSIFT(process, 0.7, 4))
            # sleep(5 * 1000L)
            # logger.debug("底部菜单栏")
            # imagesBack(home_DBCD, paramSIFT(process))
            # boolean  openBottom = ImageService.imagesBack(home_DBCDDK, paramSIFTNotClick(process, 1, 4))
            # while (!openBottom) {
            # logger.debug ("未打开底部菜单栏，点击打开")
            # imagesBack (home_DBCD, paramSIFT (process, 1, 4))
            # logger.debug("点击可能存在的返回按钮")
            # imagesBack (return_FH, paramSIFT (process, 1, 4))
            # logger.debug ("点击可能存在的下载按钮")
            # imagesBack (home_XZ, paramSIFT (process, 1, 4))
            # logger.debug("重新判断是否打开底部菜单")
            # openBottom = ImageService.imagesBack (home_DBCDDK, paramSIFTNotClick (process, 1, 4))
            # sleep (1000)
            # }
            # sleep(1000)
            # logger.debug("再次点击可能存在的下载按钮")
            # imagesBack(home_XZ, paramSIFT(process, 1, 4))
            # time.sleep(2)
            # logger.debug("当前是否是账号首页")
        logger.debug("菜单栏是否已打开")
        logger.info("初始化当前状态完成")
