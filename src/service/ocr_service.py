# @Time: 2023年08月07日 11:43
# @Author: orcakill
# @File: ocr_service.py
# @Description: 图像文字识别
import logging
import os
import re


import cv2
import numpy as np
from imageio.core import Image
from paddleocr import PaddleOCR
from pytesseract import pytesseract

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
        :param words: 文字数组或字符串
        :param exclude_words: 排除文字
        :param similarly: 相似度阈值，默认0.9
        :return: 文字坐标多边形
        """
        try:
            # 将words转换为列表，确保统一处理
            if isinstance(words, str):
                words = [words]
            
            # 将exclude_words转换为列表，确保统一处理
            if isinstance(exclude_words, str):
                exclude_words = [exclude_words]
            
            if isinstance(img, str):
                img = cv2.imread(img)
            
            logger.debug("OCR匹配参数: words={}, exclude_words={}, similarly={}".format(words, exclude_words, similarly))

            # 使用单例OCR实例进行识别（使用predict方法）
            ocr_result = get_ocr_ch().predict(img)

            if ocr_result:
                # 处理不同版本PaddleOCR的返回格式
                for line in ocr_result:
                    if not line:
                        continue
                    
                    # 新版本PaddleOCR返回字典格式
                    if isinstance(line, dict):
                        boxes = line.get('boxes', [])
                        rec_texts = line.get('rec_texts', [])
                        rec_scores = line.get('rec_scores', [])
                        
                        for i in range(len(rec_texts)):
                            if i >= len(boxes) or i >= len(rec_scores):
                                continue
                            poly = boxes[i]
                            text = rec_texts[i]
                            score = rec_scores[i]
                            
                            if poly is None or len(poly) < 4:
                                continue
                            if len(poly[0]) < 2 or len(poly[2]) < 2:
                                continue
                            
                            # 调试：记录每次匹配尝试
                            is_in_words = text in words
                            score_ok = score >= similarly
                            not_excluded = not exclude_words or text not in exclude_words
                            
                            logger.debug("匹配尝试: text='{}', in_words={}, score={} >= {}={}, not_excluded={}".format(
                                text, is_in_words, score, similarly, score_ok, not_excluded))
                            
                            condition_met = is_in_words and score_ok and not_excluded
                            
                            if condition_met:
                                logger.debug("识别到{}，置信度{}，坐标{}", text, score, poly)
                                return poly
                    else:
                        # 旧版本返回格式：[[文本区域坐标], (识别文本, 置信度)]
                        for item in line:
                            if len(item) < 2:
                                continue
                            poly = item[0]  # 文本区域坐标
                            text_info = item[1]
                            
                            # 处理不同的文本信息格式
                            if isinstance(text_info, tuple) and len(text_info) >= 2:
                                text = text_info[0]
                                score = text_info[1]
                            elif isinstance(text_info, str):
                                text = text_info
                                score = 1.0  # 默认置信度
                            else:
                                continue

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
                    if not line:
                        continue
                    if isinstance(line, dict):
                        rec_texts = line.get('rec_texts', [])
                        rec_scores = line.get('rec_scores', [])
                        for i in range(len(rec_texts)):
                            score = rec_scores[i] if i < len(rec_scores) else 0.0
                            logger.debug("{}:{}", rec_texts[i], score)
                    else:
                        for item in line:
                            if len(item) >= 2:
                                text_info = item[1]
                                if isinstance(text_info, tuple) and len(text_info) >= 2:
                                    text = text_info[0]
                                    score = text_info[1]
                                elif isinstance(text_info, str):
                                    text = text_info
                                    score = 1.0
                                else:
                                    continue
                                logger.debug("{}:{}", text, score)
        except Exception as e:
            logger.exception(e)

    @staticmethod
    def ocr_paddle_list(img, words, lang='ch'):
        """
        基于PaddleOCR的指定文字识别

        :param img: 图片路径或numpy数组
        :param words: 需要匹配的文字列表或字符串
        :param lang: 语言类型，默认中文
        :return: 包含匹配文字及其坐标的列表 [[文字, [x,y]], ...]
        """
        result_xy = []

        # 将words转换为列表，确保统一处理
        if isinstance(words, str):
            words = [words]

        if isinstance(img, str):
            img = cv2.imread(img)

        if len(img.shape) == 2:
            img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
        elif img.shape[2] == 1:
            img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)

        img = img.astype(np.uint8)

        # 使用单例OCR实例进行识别（使用predict方法）
        if lang == 'en':
            ocr_result = get_ocr_en().predict(img)
        else:
            ocr_result = get_ocr_ch().predict(img)

        if ocr_result:
            # 处理不同版本PaddleOCR的返回格式
            for line in ocr_result:
                if not line:
                    continue
                
                # 新版本PaddleOCR返回字典格式
                if isinstance(line, dict):
                    boxes = line.get('boxes', [])
                    rec_texts = line.get('rec_texts', [])
                    rec_scores = line.get('rec_scores', [])
                    
                    for i in range(len(rec_texts)):
                        if i >= len(boxes) or i >= len(rec_scores):
                            continue
                        poly = boxes[i]
                        text = rec_texts[i]
                        score = rec_scores[i]
                        
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
                else:
                    # 旧版本返回格式：[[文本区域坐标], (识别文本, 置信度)]
                    for item in line:
                        if len(item) < 2:
                            continue
                        poly = item[0]  # 文本区域坐标
                        text_info = item[1]
                        
                        # 处理不同的文本信息格式
                        if isinstance(text_info, tuple) and len(text_info) >= 2:
                            text = text_info[0]
                            score = text_info[1]
                        elif isinstance(text_info, str):
                            text = text_info
                            score = 1.0  # 默认置信度
                        else:
                            continue

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