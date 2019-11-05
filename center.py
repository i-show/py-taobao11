import os
import time
import shutil
from baidu_ocr import ocr

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


def parse(index):
    print("开始解析图像 = ", index)
    filename = "screencut_center.png"
    pull_screenshot(filename)
    word_list = ocr("{}/{}".format(LOCAL_PATH, filename))
    view_count = 0
    for word in word_list.get("words_result"):
        current_word = word["words"]
        if current_word == "去浏览" or current_word == "去查看":
            location = word["location"]
            x = location['left'] + (location['width'] / 2)
            y = location['top'] + (location['height'] / 2)
            print("当前浏览关键字为：", current_word)
            tap(int(x), int(y))
            time.sleep(2)
            os.system('adb shell input swipe 500 1700 500 1600 200')  # 先把广告拿走
            time.sleep(2)
            view_count = view_count + 1
            look_detail()
            back()
            time.sleep(2)

    if view_count > 0:
        parse(index + 1)
    else:
        print("已经浏览完毕")


if __name__ == '__main__':
    # 首先创建一个文件夹
    os.system('adb shell mkdir -p {}'.format(SD_CARD_PATH))
    shutil.rmtree(LOCAL_PATH)

    if not os.path.exists(LOCAL_PATH):
        os.makedirs(LOCAL_PATH)

    parse(1)
