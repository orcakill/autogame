# @Time: 2023年09月11日 10:30
# @Author: orcakill
# @File: impl_explore.py
# @Description: 探索
from src.model.enum import Onmyoji
from src.service.image_service import ImageService
from src.utils.my_logger import logger


def explore_chapters(game_task: []):
    """
    章节探索
    默认选择28章困难
    自动添加候补式神
    全打 打3次，有小怪打小怪，有boss打boss，都没有左右移动，检查不到小怪和boss，退出探索
    :param game_task:
    :return:
    """
    logger.debug("进入探索")
    ImageService.touch(Onmyoji.home_TS)
    logger.debug("探索")
    logger.debug("没有探索，尝试选择章节")
    logger.debug("没有探索，尝试选择困难")
    logger.debug("开始循环战斗")
    logger.debug("第一次-解锁阵容")
    logger.debug("第一次-自动候补")
    logger.debug("判断是否有小怪")
    logger.debug("判断是否有BOSS")
    logger.debug("左移3次，右移3次")
    logger.debug("退出探索")
