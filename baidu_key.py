# -*- coding: utf-8 -*-
import requests
# client_id 为官网获取的AK， client_secret 为官网获取的SK
APP_KEY = "Pa0phNdCiHRcOXkDQ3Wb2XzS"
SECRET_KEY = "dyTcS24R5y8nn0zXIvKDCv8RWwkws7rs"

host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id={}&client_secret={}'.format(APP_KEY, SECRET_KEY)
response = requests.get(host)
if response:
    print(response.json())
