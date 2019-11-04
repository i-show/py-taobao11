# -*- coding: utf-8 -*-

import cv2


def is_overlapping(store1, store2):
    left1 = store1.center[0] - store1.radius
    top1 = store1.center[1] - store1.radius
    right1 = store1.center[0] + store1.radius
    bottom1 = store1.center[1] + store1.radius

    left2 = store2.center[0] - store2.radius
    top2 = store2.center[1] - store2.radius
    right2 = store2.center[0] + store2.radius
    bottom2 = store2.center[1] + store2.radius

    return right1 > left2 and right1 < right2 and bottom1 > top2 and bottom1 < bottom2


def find_store(filename):
    img = cv2.imread(filename)
    # 灰度图像
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # 二值化
    ret, binary = cv2.threshold(gray, 175, 255, cv2.THRESH_BINARY)
    contours, hierarchy = cv2.findContours(binary, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # 以圆形框出
    store_list = []
    for i in range(len(contours)):
        (x, y), radius = cv2.minEnclosingCircle(contours[i])
        center = (int(x), int(y))
        radius = int(radius)
        # 对圆进行筛选
        if radius <= 400 and radius > 159:
            # 先进行一轮筛选
            store_list.append({"center": center, "radius": radius})
            img = cv2.circle(img, center, radius, (0, 255, 0), 2)



    print("circle = ", store_list)
    cv2.imwrite(filename.split(".")[0] + "_cv.png", img)
    return store_list
