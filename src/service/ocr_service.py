# @Time: 2023年08月07日 11:43
# @Author: orcakill
# @File: ocr_service.py
# @Description: 图像文字识别
import logging
import os
import re

import cv2
import numpy as np
from paddleocr import PaddleOCR

from src.model.enum import Onmyoji, Cvstrategy
from src.service.airtest_service import AirtestService
from src.service.impl_image_service.impl_match import ImplMatch
from src.utils.my_logger import logger

# 控制paddleocr的日志输出
log_ppocr = logging.getLogger("ppocr")
log_ppocr.setLevel(logging.CRITICAL)
os.environ['GLOG_minloglevel'] = '3'

# OCR实例缓存（单例模式）
_ocr_ch = None
_ocr_en = None


def get_ocr_ch():
    """获取中文OCR实例（单例）"""
    global _ocr_ch
    if _ocr_ch is None:
        logger.debug("初始化中文OCR模型")
        _ocr_ch = PaddleOCR(
            lang="ch",
            device='cpu',
            use_angle_cls=True,  # 启用角度分类
            text_det_thresh=0.3,  # 文本检测阈值（正确参数名）
            text_det_box_thresh=0.5,  # 文本检测框阈值
            text_det_unclip_ratio=1.6,  # 文本检测框扩展比例
            text_rec_score_thresh=0.5  # 文本识别置信度阈值
        )
    return _ocr_ch


def get_ocr_en():
    """获取英文OCR实例（单例）"""
    global _ocr_en
    if _ocr_en is None:
        logger.debug("初始化英文OCR模型")
        _ocr_en = PaddleOCR(
            lang="en",
            device='cpu',
            use_angle_cls=False
        )
    return _ocr_en


class OcrService:
    @staticmethod
    def get_word(folder_path: str, lang: str = 'chi_sim'):
        """
        获取局部截图的文本或数字信息（使用PaddleOCR）

        :param folder_path: 局部路径
        :param lang: 语言类型 eng 英语 chi_sim 简体中文
        :return: 识别到的文本
        """
        logger.debug("获取{}的位置", folder_path)
        result = ImplMatch.cv_match(folder_path, cvstrategy=Cvstrategy.default)
        if result:
            pos1 = result['rectangle'][0]
            pos2 = result['rectangle'][2]
            # 截图
            img = AirtestService.crop_image(pos1[0], pos1[1], pos2[0], pos2[1])
            
            # 使用PaddleOCR进行文字识别（替代Tesseract）
            ocr_result = get_ocr_en().predict(img) if lang == 'eng' else get_ocr_ch().predict(img)
            
            text = ""
            if ocr_result:
                for line in ocr_result:
                    rec_texts = line.get('rec_texts', [])
                    rec_scores = line.get('rec_scores', [])
                    for i in range(len(rec_texts)):
                        if i < len(rec_scores) and rec_scores[i] >= 0.5:
                            text += rec_texts[i]
            
            if text:
                # 针对特定场景的文本处理
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
                logger.debug("识别结果: {}", text)
            else:
                logger.debug("无{}", folder_path)
            return text
        else:
            logger.debug("未找到{}", folder_path)
        return None

    @staticmethod
    def re_search(pattern: str, text: str) -> str:
        """
        正则表达式搜索

        :param pattern: 正则表达式模式
        :param text: 待搜索文本
        :return: 匹配结果（始终返回str类型）
        """
        match = re.search(pattern, text)
        if match:
            return match.group()
        return ""

    @staticmethod
    def ocr_paddle(img, words, exclude_words=None, similarly=0.9):
        """
        根据图片识别文字

        :param img: 图片路径或ndarray
        :param words: 文字数组
        :param exclude_words: 排除文字
        :param similarly: 相似度阈值，默认0.9
        :return: 文字坐标多边形
        """
        try:
            if isinstance(img, str):
                img = cv2.imread(img)

            # 使用单例OCR实例进行识别
            ocr_result = get_ocr_ch().predict(img)

            if ocr_result:
                for line in ocr_result:
                    rec_texts = line.get('rec_texts', [])
                    rec_scores = line.get('rec_scores', [])
                    rec_polys = line.get('rec_polys', [])

                    for i in range(len(rec_texts)):
                        text = rec_texts[i]
                        score = rec_scores[i] if i < len(rec_scores) else 0.0

                        if i >= len(rec_polys):
                            continue

                        poly = rec_polys[i]
                        if poly is None or len(poly) < 4:
                            continue

                        if len(poly[0]) < 2 or len(poly[2]) < 2:
                            continue

                        condition_met = (
                            text in words and
                            score >= similarly and
                            (not exclude_words or text not in exclude_words)
                        )

                        if condition_met:
                            logger.debug("识别到{}，置信度{}，坐标{}", text, score, poly)
                            return poly
                logger.debug("未识别，遍历输出识别的文字信息")
                for line in ocr_result:
                    rec_texts = line.get('rec_texts', [])
                    rec_scores = line.get('rec_scores', [])
                    for i in range(len(rec_texts)):
                        if i < len(rec_scores):
                            logger.debug("{}:{}", rec_texts[i], rec_scores[i])
                        else:
                            logger.debug("{}:无置信度", rec_texts[i])
        except Exception as e:
            logger.exception(e)

    @staticmethod
    def ocr_paddle_list(img, words, lang='ch'):
        """
        基于PaddleOCR的指定文字识别

        :param img: 图片路径或numpy数组
        :param words: 需要匹配的文字列表
        :param lang: 语言类型，默认中文
        :return: 包含匹配文字及其坐标的列表 [[文字, [x,y]], ...]
        """
        result_xy = []

        if isinstance(img, str):
            img = cv2.imread(img)

        if len(img.shape) == 2:
            img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
        elif img.shape[2] == 1:
            img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)

        img = img.astype(np.uint8)

        # 使用单例OCR实例进行识别
        if lang == 'en':
            ocr_result = get_ocr_en().predict(img)
        else:
            ocr_result = get_ocr_ch().predict(img)

        if ocr_result:
            for line in ocr_result:
                rec_texts = line.get('rec_texts', [])
                rec_scores = line.get('rec_scores', [])
                rec_polys = line.get('rec_polys', [])

                min_length = min(len(rec_texts), len(rec_scores), len(rec_polys))
                if min_length == 0:
                    continue

                for i in range(min_length):
                    text = rec_texts[i]
                    score = rec_scores[i]

                    if i >= len(rec_polys):
                        continue

                    poly = rec_polys[i]
                    if poly is None or len(poly) < 4:
                        continue

                    if len(poly[0]) < 2 or len(poly[2]) < 2:
                        continue

                    if words:
                        if text in words and score >= 0.7:
                            x_center = (poly[0][0] + poly[2][0]) / 2
                            y_center = (poly[0][1] + poly[2][1]) / 2
                            if x_center > 0 and y_center > 0:
                                result_xy.append([text, [int(x_center), int(y_center)]])
                                logger.debug("识别到{}，置信度{}，坐标{}", text, score, [int(x_center), int(y_center)])
                    else:
                        if score >= 0.7:
                            x_center = (poly[0][0] + poly[2][0]) / 2
                            y_center = (poly[0][1] + poly[2][1]) / 2
                            if x_center > 0 and y_center > 0:
                                result_xy.append([text, [int(x_center), int(y_center)]])
                                logger.debug("识别到{}，置信度{}，坐标{}", text, score, [int(x_center), int(y_center)])

        return result_xy