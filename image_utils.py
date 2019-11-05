# -*- coding: utf-8 -*-

import cv2
import math


def is_overlapping(store1, store2):
    center1 = store1.get("center")
    radius1 = store1.get("radius")
    center2 = store2.get("center")
    radius2 = store2.get("radius")

    left1 = center1[0] - radius1
    top1 = center1[1] - radius1
    right1 = center1[0] + radius1
    bottom1 = center1[1] + radius1

    left2 = center2[0] - radius2
    top2 = center2[1] - radius2
    right2 = center2[0] + radius2
    bottom2 = center2[1] + radius2

    x = math.pow(abs(center1[0] - center2[0]), 2)
    y = math.pow(abs(center1[1] - center2[1]), 2)
    distance = math.sqrt(x + y)
    result = distance < radius1 + radius2
    return result


def comput_center(store_list):
    count = len(store_list)
    if count <= 0:
        return None

    first = store_list[0]
    first_center = first.get("center")
    first_radius = first.get("radius")

    minX = first_center[0] - first_radius
    minY = first_center[1] - first_radius
    maxX = first_center[0] + first_radius
    maxY = first_center[1] + first_radius
    for i in range(1, count):
        store = store_list[i]
        store_center = store.get("center")
        store_radius = store.get("radius")
        minX = min(minX, store_center[0] - store_radius)
        minY = min(minY, store_center[1] - store_radius)
        maxX = max(maxX, store_center[0] + store_radius)
        maxY = max(maxY, store_center[1] + store_radius)

    return (int((minX + maxX) / 2), int((minY + maxY) / 2))


def clear_overlapping(store_list, center_list):
    # 清除 重叠
    count = len(store_list)
    if count <= 0:
        return center_list

    store = store_list[0]
    overlapping_list = []
    overlapping_list.append(store)

    for i in range(1, count):
        _store = store_list[i]
        if is_overlapping(store, _store):
            overlapping_list.append(_store)

    center = comput_center(overlapping_list)
    if not center is None:
        center_list.append(center)

    for store in overlapping_list:
        store_list.remove(store)

    return clear_overlapping(store_list, center_list)


def find_store(filename):
    img = cv2.imread(filename)
    # 灰度图像
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # 二值化
    ret, binary = cv2.threshold(gray, 175, 255, cv2.THRESH_BINARY)
    contours, hierarchy = cv2.findContours(binary, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # 以圆形框出
    store_list = []
    center_list = []
    for i in range(len(contours)):
        (x, y), radius = cv2.minEnclosingCircle(contours[i])
        center = (int(x), int(y))
        radius = int(radius)
        # 对圆进行筛选
        if radius <= 400 and radius >= 120:
            # 先进行一轮筛选
            store_list.append({"center": center, "radius": radius})
            img = cv2.circle(img, center, radius, (0, 255, 0), 2)

    center_list = clear_overlapping(store_list, center_list)
    cv2.imwrite(filename.split(".")[0] + "_cv.png", img)
    return center_list

if __name__ == '__main__':
    find_store("image/screencut0.png")
