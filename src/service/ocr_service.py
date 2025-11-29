# @Time: 2023年08月07日 11:43
# @Author: orcakill
# @File: ocr_service.py
# @Description: 图像文字识别
import logging
import os
import re

import cv2
import numpy as np
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

ocr_ch = PaddleOCR(
    lang="ch",
    device='cpu',
    use_angle_cls=True,  # 启用角度分类
    text_det_thresh=0.3,  # 文本检测阈值（正确参数名）
    text_det_box_thresh=0.5,  # 文本检测框阈值
    text_det_unclip_ratio=1.6,  # 文本检测框扩展比例
    text_rec_score_thresh=0.5  # 文本识别置信度阈值
)

ocr_en = PaddleOCR(
    lang="en",
    device='cpu',
    use_angle_cls=False
)


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
        # 如果是文件路径，读取图像
        try:
            if isinstance(img, str):
                img = cv2.imread(img)

            # 保存原始图像用于后续绘制矩形
            original_img = img.copy()

            # 图像预处理：灰度化、二值化、降噪
            if len(img.shape) == 3:
                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            else:
                gray = img

            # 二值化处理
            _, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

            # 降噪
            kernel = np.ones((2, 2), np.uint8)
            processed_img = cv2.morphologyEx(binary, cv2.MORPH_OPEN, kernel)

            # 修复：确保图像是三通道的RGB格式
            if len(processed_img.shape) == 2:  # 如果是灰度图
                processed_img = cv2.cvtColor(processed_img, cv2.COLOR_GRAY2BGR)
            elif processed_img.shape[2] == 1:  # 如果是单通道
                processed_img = cv2.cvtColor(processed_img, cv2.COLOR_GRAY2BGR)

            # 确保图像数据类型是uint8
            processed_img = processed_img.astype(np.uint8)

            # 使用预处理后的图像进行OCR
            ocr_result = ocr_ch.predict(processed_img)

            if ocr_result:
                for line in ocr_result:
                    rec_texts = line.get('rec_texts', [])  # 识别到的文字
                    rec_scores = line.get('rec_scores', [])  # 置信度得分
                    rec_polys = line.get('rec_polys', [])  # 文字位置坐标

                    # 遍历每个识别到的文字
                    for i in range(0, len(rec_texts)):
                        text = rec_texts[i]
                        score = rec_scores[i] if i < len(rec_scores) else 0.0

                        # 修复：添加多边形数据有效性检查
                        if i >= len(rec_polys):
                            continue

                        poly = rec_polys[i]
                        # 修复：使用正确的方式检查numpy数组
                        if poly is None or len(poly) < 4:
                            continue

                        # 检查多边形坐标点是否完整
                        if len(poly[0]) < 2 or len(poly[2]) < 2:
                            continue

                        # 统一条件判断
                        condition_met = (
                                text in words and
                                score >= similarly and
                                (not exclude_words or text not in exclude_words)
                        )

                        if condition_met:
                            x_center = (poly[0][0] + poly[2][0]) / 2
                            y_center = (poly[0][1] + poly[2][1]) / 2
                            if x_center > 0 and y_center > 0:
                                # logger.debug("识别到{}，置信度{}，坐标{}", text, score, (int(x_center), int(y_center)))
                                # AirtestService.draw_rectangle(original_img, int(x_center - 20), int(y_center - 20),
                                #                               int(x_center + 20), int(y_center + 20))
                                return int(x_center), int(y_center)
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
        :param lang:
        :param img: 图片路径或numpy数组
        :param words: 需要匹配的文字列表
        :return: 包含匹配文字及其坐标的列表 [[文字, [x,y]], ...]
        """
        result_xy = []

        # 修复：确保图像是三通道的
        if isinstance(img, str):
            img = cv2.imread(img)

        if len(img.shape) == 2:  # 如果是灰度图
            img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
        elif img.shape[2] == 1:  # 如果是单通道
            img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)

        # 确保图像数据类型是uint8
        img = img.astype(np.uint8)

        # 执行OCR识别
        ocr_result = ocr_ch.predict(img)
        if lang == 'en':
            ocr_result = ocr_en.predict(img)

        if ocr_result:
            # 解析识别结果
            for line in ocr_result:
                # 使用安全字典访问
                rec_texts = line.get('rec_texts', [])  # 识别到的文字
                rec_scores = line.get('rec_scores', [])  # 置信度得分
                rec_polys = line.get('rec_polys', [])  # 文字位置坐标

                # 检查数组长度是否匹配
                min_length = min(len(rec_texts), len(rec_scores), len(rec_polys))
                if min_length == 0:
                    continue

                # 遍历每个识别到的文字
                for i in range(min_length):
                    text = rec_texts[i]
                    score = rec_scores[i]

                    # 检查多边形数据有效性
                    if i >= len(rec_polys):
                        continue

                    poly = rec_polys[i]
                    # 修复：使用正确的方式检查numpy数组
                    if poly is None or len(poly) < 4:
                        continue

                    # 检查多边形坐标点是否完整
                    if len(poly[0]) < 2 or len(poly[2]) < 2:
                        continue

                    # 与目标文字列表比对
                    if words:
                        if text in words and score >= 0.7:  # 降低置信度阈值以提高识别率
                            # 计算中心坐标
                            x_center = (poly[0][0] + poly[2][0]) / 2
                            y_center = (poly[0][1] + poly[2][1]) / 2
                            if x_center > 0 and y_center > 0:
                                # 使用列表格式的坐标
                                result_xy.append([text, [int(x_center), int(y_center)]])
                                logger.debug("识别到{}，置信度{}，坐标{}", text, score, [int(x_center), int(y_center)])
                    else:
                        if score >= 0.7:  # 降低置信度阈值以提高识别率
                            # 计算中心坐标
                            x_center = (poly[0][0] + poly[2][0]) / 2
                            y_center = (poly[0][1] + poly[2][1]) / 2
                            if x_center > 0 and y_center > 0:
                                # 使用列表格式的坐标
                                result_xy.append([text, [int(x_center), int(y_center)]])
                                logger.debug("识别到{}，置信度{}，坐标{}", text, score, [int(x_center), int(y_center)])

        return result_xy