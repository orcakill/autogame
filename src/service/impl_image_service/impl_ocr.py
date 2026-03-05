# @Time: 2024年06月19日 15:26
# @Author: orcakill
# @File: impl_ocr.py
# @Description: 图像文字识别
from src.service.airtest_service import AirtestService
from src.service.ocr_service import OcrService
from src.utils.my_logger import logger


class ImplOcr:
    @staticmethod
    def ocr_touch(words, exclude_words=None,similarly=0.9):
        logger.debug("获取当前页面截图")
        screen = AirtestService.snapshot()
        try:
            if screen is not None:
                pos=None
                logger.debug("全图检查文字坐标:{}",words)
                poly= OcrService.ocr_paddle(screen, words, exclude_words, similarly)
                if poly is not None:
                    # 验证区域内是否能识别到文字
                    logger.debug("局部截图验证文字坐标:{}", words)
                    x_min = min(poly[:, 0])  # 所有x坐标的最小值
                    y_min = min(poly[:, 1])  # 所有y坐标的最小值
                    x_max = max(poly[:, 0])  # 所有x坐标的最大值
                    y_max = max(poly[:, 1])  # 所有y坐标的最大值
                    screen_crop = AirtestService.crop_image(x_min*0.9, y_min*0.9, x_max*1.1, y_max*1.1,screen)
                    # AirtestService.draw_rectangle(screen,x_min*0.9, y_min*0.9, x_max*1.1, y_max*1.1)
                    poly_crop = OcrService.ocr_paddle(screen_crop, words, exclude_words, similarly)
                    if poly_crop is not None:
                        logger.debug("识别并验证文字{}坐标成功，坐标区域{}", words, poly)
                        x_center = (x_min + x_max) / 2
                        y_center = (y_min + y_max) / 2
                        if x_center > 0 and y_center > 0:
                            logger.debug("计算坐标成功，文字{}，坐标{}", words, (int(x_center), int(y_center)))
                            pos = (int(x_center), int(y_center))
                if pos:
                    logger.debug("点击文字坐标:{}", words)
                    AirtestService.touch_coordinate(pos)
                    return True
                else:
                    logger.debug("未识别到文字坐标:{}", words)
            else:
                logger.debug("未截取到图片")
        except Exception as e:
            logger.exception("异常{}", e)
        return False

    @staticmethod
    def ocr_list(words,lang='ch'):
        result = []
        logger.debug("获取当前页面截图")
        screen = AirtestService.snapshot()
        try:
            if screen is not None:
                logger.debug("检查文字坐标:{}", str(words))
                result = OcrService.ocr_paddle_list(screen, words,lang)
            else:
                logger.debug("未截取到图片")
        except Exception as e:
            logger.error("异常{}", e)
        return result