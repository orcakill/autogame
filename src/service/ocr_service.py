# @Time: 2023年08月07日 11:43
# @Author: orcakill
# @File: ocr_service.py
# @Description: 图像文字识别
import logging
import os
import re

import pytesseract
from paddleocr import PaddleOCR

from src.model.enum import Onmyoji, Cvstrategy
from src.service.airtest_service import AirtestService
from src.service.impl_image_service.impl_match import ImplMatch
from src.utils.my_logger import logger

# 控制paddleocr的日志输出
log_ppocr = logging.getLogger("ppocr")
log_ppocr.setLevel(logging.CRITICAL)
os.environ['GLOG_minloglevel'] = '3'

ocr_ch = PaddleOCR(lang="ch", device='cpu')
ocr_en = PaddleOCR(lang="en", device='cpu')


class OcrService:
    @staticmethod
    def get_word(folder_path: str, lang: str = 'eng'):
        """
        获取局部截图的文本或数字信息

        :param folder_path: 局部路径
        :param lang: 语言类型 eng  英语 chi_sim 简体中文
        :return:
        """
        # 结界突破区域
        logger.debug("获取{}的位置", folder_path)
        result = ImplMatch.cv_match(folder_path, cvstrategy=Cvstrategy.default)
        if result:
            pos1 = result['rectangle'][0]
            pos2 = result['rectangle'][2]
            # 截图
            img = AirtestService.crop_image(pos1[0], pos1[1], pos2[0], pos2[1])
            # 图像文字识别
            pil_image = AirtestService.cv2_2_pil(img)
            # pil_image.save("D:/a.png", quality=99, optimize=True)
            # image = Image.open('D:/a.png')
            # 打开图像
            image = pil_image.convert('RGBA')
            # 使用 Tesseract 进行文字识别
            text = pytesseract.image_to_string(image, lang=lang)
            if text and text is not None:
                if folder_path == Onmyoji.border_JJTZJQY:
                    text = OcrService.re_search(r'\d+(?=/30)', text)
                if folder_path == Onmyoji.friends_HYSQY:
                    text = OcrService.re_search(r'\d+(?=/200)', text)
                if folder_path == Onmyoji.deed_MQSS:
                    text = OcrService.re_search(r'\d+(?=/30)', text)
                if folder_path == Onmyoji.explore_DQLHSL:
                    text = OcrService.re_search(r'\d+(?=/50)', text)
                if folder_path == Onmyoji.region_TZCS:
                    text = OcrService.re_search(r'\d+(?=/6)', text)
                if folder_path == Onmyoji.foster_JJK_GYWZ:
                    text = text.split('+')[-1].strip() if '+' in text else text
            if text:
                logger.debug(text)
            else:
                logger.debug("无{}", folder_path)
            return text
            # 文字判断
        else:
            logger.debug("未找到{}", folder_path)
        return None

    @staticmethod
    def re_search(pattern: str, text: str):
        text = re.search(pattern, text)
        if text:
            text = text.group()
        return text

    @staticmethod
    def ocr_paddle(img, words, exclude_words=None, similarly=0.9):
        """
        根据图片识别文字
        :param similarly:0.9
        :param exclude_words: 排除文字
        :param img: 图片   路径或ndarray
        :param words: 文字数组
        :return: 文字坐标
        """
        pos = ""

        # 执行OCR识别
        ocr_result = ocr_ch.predict(img)

        if ocr_result:
            for line in ocr_result:
                rec_texts = line['rec_texts']  # 识别到的文字
                rec_scores = line['rec_scores']  # 置信度得分
                rec_polys = line['rec_polys']  # 文字位置坐标

                # 遍历每个识别到的文字
                for i in range(0, len(rec_texts)):
                    text = rec_texts[i]
                    score = rec_scores[i]
                    # 统一条件判断
                    condition_met = (
                            text in words and
                            score >= 0.9 and
                            (not exclude_words or text not in exclude_words)
                    )

                    if condition_met:
                        poly = rec_polys[i]
                        x_center = (poly[0][0] + poly[2][0]) / 2
                        y_center = (poly[0][1] + poly[2][1]) / 2
                        if x_center > 0 and y_center > 0:
                            return (int(x_center), int(y_center))
        logger.debug("未识别，遍历输出识别的文字信息")
        for line in ocr_result:
            rec_texts = line['rec_texts']  # 识别到的文字
            rec_scores = line['rec_scores']
            # 遍历每个识别到的文字
            for i in range(len(rec_texts)):
                logger.debug("{}:{}", rec_texts[i], rec_scores[i])
        return None

    @staticmethod
    def ocr_paddle_list(img, words, lang='ch'):
        """
        基于PaddleOCR的指定文字识别
        :param lang:
        :param img: 图片路径或numpy数组
        :param words: 需要匹配的文字列表
        :return: 包含匹配文字及其坐标的列表 [[文字, (x,y)], ...]
        """
        result_xy = []

        # 执行OCR识别
        ocr_result = ocr_ch.predict(img)
        if lang == 'en':
            ocr_result = ocr_en.predict(img)
        if ocr_result:
            # 解析识别结果
            for line in ocr_result:
                rec_texts = line['rec_texts']  # 识别到的文字
                rec_scores = line['rec_scores']  # 置信度得分
                rec_polys = line['rec_polys']  # 文字位置坐标

                # 遍历每个识别到的文字
                for i in range(0, len(rec_texts)):
                    # 与目标文字列表比对
                    if words:
                        if rec_texts[i] in words and rec_scores[i] >= 0.9:
                            # 计算中心坐标
                            poly = rec_polys[i]
                            x_center = (poly[0][0] + poly[2][0]) / 2
                            y_center = (poly[0][1] + poly[2][1]) / 2
                            result_xy.append([rec_texts[i], (int(x_center), int(y_center))])
                    else:
                        if rec_scores[i] >= 0.9:
                            # 计算中心坐标
                            poly = rec_polys[i]
                            x_center = (poly[0][0] + poly[2][0]) / 2
                            y_center = (poly[0][1] + poly[2][1]) / 2
                            result_xy.append([rec_texts[i], (int(x_center), int(y_center))])
        return result_xy
