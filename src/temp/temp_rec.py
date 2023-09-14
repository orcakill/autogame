"""
# @Time: 2023年09月15日00:19
# @Author: orcakill
# @File: temp_rec.py
# @Description: 测试相似度计算
"""

from airtest.aircv.cal_confidence import *


if __name__ == '__main__':
    img1 = cv2.imread(r"D:\\a.png")
    img2 = cv2.imread(r"D:\\b.png")
    img3 = cv2.imread(r"D:\\c.png")
    img4 = cv2.imread(r"D:\\d.png")
    img5 = cv2.imread(r"D:\\e.png")

    print(cal_ccoeff_confidence(img1, img2))
    print(cal_ccoeff_confidence(img1, img3))
    print(cal_ccoeff_confidence(img1, img4))
    print(cal_ccoeff_confidence(img1, img5))
