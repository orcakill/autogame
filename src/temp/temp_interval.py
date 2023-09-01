"""
# @Time: 2023年08月26日22:45
# @Author: orcakill
# @File: temp_interval.py
# @Description: 间隔计算
"""
from src.model.enum import Onmyoji
from src.service.complex_service import ComplexService
from src.service.image_service import ImageService
from src.service.ocr_service import OcrService
from src.utils.my_logger import logger

# 服务接口
image_service = ImageService()
complex_service = ComplexService()
ocr_service = OcrService()

if __name__ == '__main__':
    image_service.auto_setup("0")
    logger.debug("测试-确定上方好友坐标")
    coordinate_friend = image_service.exists(Onmyoji.foster_SFHY)
    logger.debug("测试-确定上方跨区坐标")
    coordinate_region = image_service.exists(Onmyoji.foster_SFKQ)
    logger.debug("测试-计算位置1")
    coordinate_difference = 0.9*(coordinate_region[0] - coordinate_friend[0])
    coordinate_start = (coordinate_region[0], coordinate_region[1] + coordinate_difference)
    logger.debug("测试-计算位置2")
    coordinate_end = (coordinate_region[0], coordinate_region[1] + 2 * coordinate_difference)
    c1 = coordinate_end[1] - coordinate_start[1]
    logger.debug("coordinate_start:", coordinate_start)
    logger.debug("coordinate_end:", coordinate_end)
    logger.debug("c1:", c1)
    coordinate_text1 = image_service.exists(r"活动\20230823\爬塔\测试1")
    coordinate_text2 = image_service.exists(r"活动\20230823\爬塔\测试2")
    c2 = coordinate_text2[1] - coordinate_text1[1]
    logger.debug("coordinate_text1:", coordinate_text1)
    logger.debug("coordinate_text2:", coordinate_text2)
    logger.debug("c2:", c2)
