# @Time: 2024年03月07日 11:11
# @Author: orcakill
# @File: prop.py
# @Description: 道聚城每日签到，领取交易牌，领取每日充值奖励
from src.model.enum import Onmyoji
from src.service.airtest_service import AirtestService
from src.service.image_service import ImageService
from src.utils.my_logger import logger


def prop():
    logger.debug("启动道聚城,每日奖励")
    ImageService.restart_app("com.tencent.djcity")
    logger.debug("检查签到")
    for i in range(5):
        logger.debug("点击跳过")
        ImageService.touch(Onmyoji.prop_TG)
        logger.debug("点击好的")
        ImageService.touch(Onmyoji.prop_HD)
        logger.debug("点击叉号")
        ImageService.touch(Onmyoji.prop_CH)
        logger.debug("点击我的游戏")
        ImageService.touch(Onmyoji.prop_WDYX)
        logger.debug("每日充值")
        ImageService.touch(Onmyoji.prop_MRCZ)
        logger.debug("领取")
        ImageService.touch(Onmyoji.prop_LQ)
    logger.debug("启动道聚城,签到任务")
    ImageService.restart_app("com.tencent.djcity")
    logger.debug("检查签到")
    for i in range(5):
        logger.debug("点击跳过")
        ImageService.touch(Onmyoji.prop_TG)
        logger.debug("点击好的")
        ImageService.touch(Onmyoji.prop_HD)
        logger.debug("点击叉号")
        ImageService.touch(Onmyoji.prop_CH)
    logger.debug("关闭道聚城")
    ImageService.stop_app("com.tencent.djcity")


if __name__ == '__main__':
    AirtestService.auto_setup("0")
    prop()
