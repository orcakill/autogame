"""
# @Time: 2023年08月31日01:24
# @Author: orcakill
# @File: impl_return_home.py
# @Description: 返回首页
"""
import os

from src.model.enum import Onmyoji
from src.model.models import GameAccount
from src.service.complex_service import ComplexService
from src.service.image_service import ImageService
from src.service.ocr_service import OcrService
from src.utils.my_logger import logger

# 服务接口
image_service = ImageService()
complex_service = ComplexService()
ocr_service = OcrService()


def return_home(game_task: []):
    game_account = GameAccount(game_task[2])
    # 判断是否是待登录账号首页
    logger.debug("返回首页-判断当前状态")
    # 当前状态 账号首页 1，2,3，4，5
    #        其它，不在账号首页
    account_index = os.path.join(Onmyoji.user_SYTX, game_account.id)
    is_index = image_service.exists(account_index)
    is_explore = image_service.exists(Onmyoji.home_TS)
    if not is_index or not is_explore:
        logger.debug("判断是否在桌面")
        is_desktop = image_service.exists(Onmyoji.login_YYSTB)
        if not is_desktop:
            logger.debug("不在账号首页且不是桌面，循环5次，5次不成功则返回失败")
            # 获取返回列表
            for i_return in range(5):
                logger.debug("点击可能存在的返回按钮")
                image_service.touch(Onmyoji.comm_FH_ZSJLDYXBSXYH)
                image_service.touch(Onmyoji.comm_FH_ZSJLDBKBSXYH)
                image_service.touch(Onmyoji.comm_FH_YSJHDBSCH)
                image_service.touch(Onmyoji.comm_FH_XSFYHSCH)
                image_service.touch(Onmyoji.comm_FH_YSJZDHBSCH)
                image_service.touch(Onmyoji.comm_FH_ZSJHKHSXYH)
                image_service.touch(Onmyoji.comm_FH_ZSJZKDZSHXJT)
                image_service.touch(Onmyoji.comm_FH_ZSJHKZDHSXYH)
                logger.debug("点击可能存在的退出挑战")
                image_service.touch(Onmyoji.soul_BQ_TCTZ)
                logger.debug("重新判断是否返回首页")
                is_index = image_service.exists(account_index)
                is_explore = image_service.exists(Onmyoji.home_TS)
                if is_index and is_explore:
                    logger.debug("返回首页成功")
                    return True
        else:
            logger.debug("在桌面，重新登录")
            return False
    else:
        logger.debug("有探索，有账号，在首页")
        return True
    return False
