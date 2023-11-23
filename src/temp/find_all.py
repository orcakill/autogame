"""
# @Time: 2023年09月04日00:59
# @Author: orcakill
# @File: find_all.py
# @Description: 寻找数量
"""
from airtest.core.helper import G

from src.service.image_service import ImageService
from src.utils.my_logger import my_logger as logger

if __name__ == '__main__':
    logger.debug("开始")
    ImageService.auto_setup("1")
    t=G.DEVICE_LIST
    logger.debug(t)
