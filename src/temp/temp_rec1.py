import cv2
from airtest.aircv.cal_confidence import cal_ccoeff_confidence
from airtest.core.cv import Template


if __name__ == '__main__':
    # 加载两个模板图片
    template1 = Template("D:\\a.png")
    template2 = Template("D:\\b.png")

    img1 = cv2.imread(template1.filename)
    img2 = cv2.imread(template2.filename)

    # 比较两个模板的相似度
    confidence = cal_ccoeff_confidence(img1,img2)

    # 输出相似度
    print("两个模板的相似度：", confidence)
