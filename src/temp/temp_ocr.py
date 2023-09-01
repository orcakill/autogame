# @Time: 2023年08月07日 10:56
# @Author: orcakill
# @File: temp_ocr.py
# @Description: 图像文字识别

import pytesseract
from PIL import Image


def fun1():
    # 打开图像
    image = Image.open('d:\\a.png')

    # 使用 Tesseract 进行文字识别
    text = pytesseract.image_to_string(image, lang='eng')

    # 打印识别结果
    print(text)


if __name__ == '__main__':
    fun1()