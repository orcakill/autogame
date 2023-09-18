import cv2
import numpy as np

if __name__ == '__main__':
    # 读取大图和小图
    large_image = cv2.imread('D:/a.png')
    small_image = cv2.imread('D:/b.png')

    # 获取小图尺寸
    small_height, small_width, _ = small_image.shape

    # 创建SIFT对象并计算关键点和描述符
    sift = cv2.SIFT_create()
    kp1, des1 = sift.detectAndCompute(small_image, None)
    kp2, des2 = sift.detectAndCompute(large_image, None)

    # 创建BFMatcher对象并进行匹配
    bf = cv2.BFMatcher()
    matches = bf.knnMatch(des1, des2, k=2)

    # 应用比值测试，筛选出好的匹配点
    good_matches = []
    for m, n in matches:
        if m.distance < 0.7 * n.distance:
            good_matches.append(m)

    # 计算边框中心点坐标
    if len(good_matches) > 4:
        src_pts = np.float32([kp1[m.queryIdx].pt for m in good_matches]).reshape(-1, 1, 2)
        dst_pts = np.float32([kp2[m.trainIdx].pt for m in good_matches]).reshape(-1, 1, 2)
        M, _ = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 5.0)
        h, w, _ = small_image.shape
        corners = np.float32([[0, 0], [0, h - 1], [w - 1, h - 1], [w - 1, 0]]).reshape(-1, 1, 2)
        transformed_corners = cv2.perspectiveTransform(corners, M)
        transformed_corners += (
        large_image.shape[1] // 2 - small_width // 2, large_image.shape[0] // 2 - small_height // 2)
        cv2.polylines(large_image, [np.int32(transformed_corners)], True, (0, 0, 255), 2)

    # 在D盘上保存新图片
    cv2.imwrite('D:/path_to_output_image.jpg', large_image)

