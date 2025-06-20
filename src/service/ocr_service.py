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
    def ocr_paddle(img, words):
        """
        根据图片识别文字
        :param img: 图片   路径或ndarray
        :param words: 文字数组
        :return: 文字坐标
        """
        pos = ""
        # 初始化OCR引擎
        ocr = PaddleOCR(lang="ch", device='cpu')  # 使用中文模型，CPU模式

        # 执行OCR识别
        ocr_result = ocr.predict(img)

        if ocr_result:
            rec_texts = ocr_result['rec_texts']  # 识别到的文字
            rec_scores = ocr_result['rec_scores']  # 置信度得分
            rec_polys = ocr_result['rec_polys']  # 文字位置坐标

            # 遍历每个识别到的文字
            for i in range(len(rec_texts)):
                for word in words:
                    if rec_texts[i] == word and rec_scores[i] >= 0.9:
                        # 计算中心坐标
                        poly = rec_polys[i]
                        x_center = (poly[0][0] + poly[2][0]) / 2
                        y_center = (poly[0][1] + poly[2][1]) / 2
                        if x_center > 0 and y_center > 0:
                            pos = (int(x_center), int(y_center))
                            return pos

        if pos == "":
            logger.debug("未识别，遍历输出识别的文字信息")
            for line in ocr_result:
                rec_texts = line['rec_texts']  # 识别到的文字
                # 遍历每个识别到的文字
                for i in range(len(rec_texts)):
                    logger.debug("{}:{}", rec_texts[i])
        return pos

    @staticmethod
    def ocr_paddle_list(img, words):
        """
        基于PaddleOCR的指定文字识别
        :param img: 图片路径或numpy数组
        :param words: 需要匹配的文字列表
        :return: 包含匹配文字及其坐标的列表 [[文字, (x,y)], ...]
        """
        result_xy = []
        # 初始化OCR引擎
        ocr = PaddleOCR(lang="ch", device='cpu')  # 使用中文模型，CPU模式

        # 执行OCR识别
        ocr_result = ocr.predict(img)

        if ocr_result:
            # 解析识别结果
            for line in ocr_result:
                rec_texts = line['rec_texts']  # 识别到的文字
                rec_scores = line['rec_scores']  # 置信度得分
                rec_polys = line['rec_polys']  # 文字位置坐标

                # 遍历每个识别到的文字
                for i in range(len(rec_texts)):
                    # 与目标文字列表比对
                    for word in words:
                        if rec_texts[i] == word and rec_scores[i] >= 0.9:
                            # 计算中心坐标
                            poly = rec_polys[i]
                            x_center = (poly[0][0] + poly[2][0]) / 2
                            y_center = (poly[0][1] + poly[2][1]) / 2
                            result_xy.append([word, (int(x_center), int(y_center))])
        return result_xy

    @staticmethod
    def ocr_paddle_all(img):
        """
        识别图片中的所有文字
        :param img: 图片路径或numpy数组
        :return: 包含所有文字及其坐标的列表 [[文字, (x,y)], ...]
        """
        result_xy = []
        # 初始化OCR引擎
        ocr = PaddleOCR(lang="ch", device='cpu')

        # 执行OCR识别
        ocr_result = ocr.predict(img)

        if ocr_result:
            # 解析识别结果
            for line in ocr_result:
                rec_texts = line['rec_texts']
                rec_scores = line['rec_scores']
                rec_polys = line['rec_polys']

                # 过滤低置信度结果
                for i in range(len(rec_texts)):
                    if rec_scores[i] >= 0.9:
                        # 计算中心坐标
                        poly = rec_polys[i]
                        x_center = (poly[0][0] + poly[2][0]) / 2
                        y_center = (poly[0][1] + poly[2][1]) / 2
                        result_xy.append([rec_texts[i], (int(x_center), int(y_center))])
        return result_xy

    @staticmethod
    def ocr_paddle_xs(results, exclude_name, heroes_list):
        """
        筛选关联结果
        :param results: OCR识别结果
        :param exclude_name: 需要排除的英雄名
        :param heroes_list: 英雄列表
        :return: 筛选后的结果 [[英雄名, 关联数据], ...]
        """
        filtered_results = []
        # 遍历所有英雄
        for hero in heroes_list:
            # 跳过排除的英雄
            if hero == exclude_name:
                continue

            # 遍历识别结果
            for i in range(len(results) - 1):  # 防止越界
                # 检查英雄名是否在结果中
                if hero in results[i][0]:
                    filtered_results.append([hero, results[i + 1][0]])
        return filtered_results
