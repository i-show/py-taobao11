# -*- coding: utf-8 -*-

# 有效期为30天---请自行获取
# 参考  https://ai.baidu.com/docs#/OCR-API-Access/top

access_token = "24.dc55b8541c66ef21f679c37f045c8c89.2592000.1575427054.282335-17685641"

import base64
import requests

url = "https://aip.baidubce.com/rest/2.0/ocr/v1/general_basic"

def get_code(img_path):
    print("店铺的图片信息 = ", img_path)
    header = {
        "Content-Type": "application/x-www-form-urlencoded"
    }

    def read_img():
        with open(img_path, "rb")as f:
            return base64.b64encode(f.read()).decode()

    image = read_img()
    response = requests.post(url=url, data={"image": image, "access_token": access_token}, headers=header)
    res_json = response.json()
    res_str = ""
    for word in res_json.get("words_result"):
        res_str += word.get("words")
    return res_str

if __name__ == '__main__':
    res = get_code('detial.png')
    print(res)
