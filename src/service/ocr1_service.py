# -*- coding: utf-8 -*-
# 导入必要的库
import datetime  # 日期时间处理
import json  # JSON数据解析
import os  # 操作系统接口
import cv2  # OpenCV图像处理
import numpy as np  # 数值计算
import requests  # HTTP请求
from paddleocr import PaddleOCR  # 百度PaddleOCR文字识别

# 设置环境变量
os.environ['GLOG_minloglevel'] = '3'  # 关闭PaddleOCR的冗余日志
os.environ['PATH'] = 'D:\\software\\ccache;' + os.environ['PATH']  # 添加ccache路径
os.environ['CMAKE_C_COMPILER_LAUNCHER'] = 'ccache'  # 配置C编译器缓存
os.environ['CMAKE_CXX_COMPILER_LAUNCHER'] = 'ccache'  # 配置C++编译器缓存


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


def get_honor_of_kings_heroes():
    """
    获取王者荣耀全英雄列表
    :return: 英雄名字列表
    """
    api_url = 'https://pvp.qq.com/web201605/js/herolist.json'
    try:
        # 发送HTTP请求
        response = requests.get(api_url, timeout=10)
        response.encoding = 'utf-8'  # 强制使用UTF-8编码

        if response.status_code == 200:
            # 解析JSON数据
            heroes_data = json.loads(response.text)
            return [hero['cname'] for hero in heroes_data]
        return []
    except Exception as e:
        print(f"英雄列表请求失败: {e}")
        return []


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


if __name__ == '__main__':
    # 记录开始时间
    start_time = datetime.datetime.now()

    # 读取图片文件
    with open("1.jpg", "rb") as f:
        # 解码图片为numpy数组
        img_array1 = cv2.imdecode(np.frombuffer(f.read(), np.uint8), cv2.IMREAD_COLOR)

    with open("2.jpg", "rb") as f:
        img_array2 = cv2.imdecode(np.frombuffer(f.read(), np.uint8), cv2.IMREAD_COLOR)

    # 获取英雄列表
    hero_list = get_honor_of_kings_heroes()

    # 执行OCR识别
    result_img1 = ocr_paddle_list(img_array1, hero_list)  # 图片1识别
    result_img2 = ocr_paddle_all(img_array2)  # 图片2识别

    # 筛选关联结果
    final_result = ocr_paddle_xs(result_img2, '东皇太一', hero_list)

    # 输出结果
    print("图片1识别结果:", result_img1)
    print("图片2筛选结果:", final_result)

    # 计算执行时间
    print("总耗时:", datetime.datetime.now() - start_time)