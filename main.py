# -*- coding: utf-8 -*-
import os
import time
import shutil
from image_utils import find_store
from baidu_ocr import get_code

SD_CARD_PATH = "/sdcard/aaATaoBao1111"
LOCAL_PATH = "image"

def pull_screenshot(filname):
    os.system('adb shell screencap -p {}/{}'.format(SD_CARD_PATH, filname))
    os.system('adb pull {}/{} ./{}'.format(SD_CARD_PATH, filname, LOCAL_PATH))
    return filname

def swipe_up(px=1350):
    os.system('adb shell input swipe 100 {} 100 100 500'.format(1350 + 100))

def tap(x=0, y=0):
    os.system('adb shell input tap {x} {y}'.format(x=x, y=y))

def back():
    os.system('adb shell input keyevent 4')

def look_detail():
    for i in range(4):
        os.system('adb shell input swipe 200 1000 200 100 500')
        time.sleep(4)

if __name__ == '__main__':
    # 首先创建一个文件夹
    os.system('adb shell mkdir -p {}'.format(SD_CARD_PATH))
    shutil.rmtree(LOCAL_PATH)

    if not os.path.exists(LOCAL_PATH):
        os.makedirs(LOCAL_PATH)

    circle_index = 0
    # 手动进入首屏
    for i in range(4):
        # 滑动到店铺列表
        swipe_up()
        time.sleep(3)
        filename = "screencut{}.png".format(str(i))
        print("开始解析图像")
        pull_screenshot(filename)
        # 分析图像
        store_list = find_store("{}/{}".format(LOCAL_PATH, filename))
        print("当前准备逛的店铺有", len(store_list), "家")
        for store in store_list:
            xy_point = store.get("center")
            x_point = xy_point[0]
            y_point = xy_point[1]
            # 进入店铺
            print("********** 进入店铺 ***************")
            tap(x=x_point, y=y_point)
            time.sleep(1.5)
            swipe_up()# 先把广告拿走

            # 判断是否逛过
            detial_file_name = 'detial_{}_{}.png'.format(i, circle_index)
            pull_screenshot(detial_file_name)
            res = get_code("{}/{}".format(LOCAL_PATH, detial_file_name))
            # print("OCR 识别结果：", res)
            if '今日已达上限' in res:
                import sys
                print("今日已达上限")
                sys.exit()
            if "任务完成" in res or "继续逛逛吧" in res:
                back()
            else:
                print("逛店中...")
                look_detail()
                back()

            circle_index = circle_index + 1
            time.sleep(3)
