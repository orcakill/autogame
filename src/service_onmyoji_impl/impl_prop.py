# @Time: 2024年03月07日 11:11
# @Author: orcakill
# @File: prop.py
# @Description: 道聚城每日签到，领取交易牌，领取每日充值奖励
from src.model.enum import Onmyoji
from src.service.airtest_service import AirtestService
from src.service.image_service import ImageService
from src.utils.my_logger import logger


def prop():
    logger.debug("启动道聚城")
    ImageService.restart_app("com.tencent.djcity")
    logger.debug("检查签到")
    for i in range(10):
        is_sign_in = ImageService.exists(Onmyoji.prop_QD)
        if is_sign_in:
            break
        else:
            logger.debug("点击跳过")
            ImageService.exists(Onmyoji.prop_TG)
            logger.debug("点击好的")
            ImageService.exists(Onmyoji.prop_HD)
            logger.debug("点击叉号")
            ImageService.exists(Onmyoji.prop_CH)
    for i in range(5):
        logger.debug("点击我的游戏")
        ImageService.exists(Onmyoji.prop_WDYX)
        logger.debug("每日充值")
        ImageService.exists(Onmyoji.prop_MRCZ)
        logger.debug("领取")
        is_get = ImageService.exists(Onmyoji.prop_LQ)
        if is_get:
            break
    logger.debug("关闭道聚城")
    ImageService.stop_app("com.tencent.djcity")


if __name__ == '__main__':
    AirtestService.auto_setup("0")
    prop()
