# pip install alibabacloud_dingtalk


import sys

from typing import List

from alibabacloud_dingtalk.oauth2_1_0.client import Client as dingtalkoauth2_1_0Client
from alibabacloud_tea_openapi import models as open_api_models
from alibabacloud_dingtalk.oauth2_1_0 import models as dingtalkoauth_2__1__0_models
from alibabacloud_tea_util.client import Client as UtilClient



import alibabacloud_dingtalk

import requests
import json




app_key='ding8vpsqgzogb6voupx'
app_secret = 'RLSGybKH2ZaJdrxqDzcNknhLEdYkqPF1f64f5Jo2DI7zb-RTg-SVZvlvgIMI14lo'

def get_access_token():
    config = open_api_models.Config()
    config.protocol = 'https'
    config.region_id = 'central'
    client = dingtalkoauth2_1_0Client(config)
    get_access_token_request = dingtalkoauth_2__1__0_models.GetAccessTokenRequest(
        app_key=app_key,
        app_secret=app_secret
    )
    try:
        access_token = client.get_access_token(get_access_token_request).body
        return access_token
    except Exception as err:
        if not UtilClient.empty(err.code) and not UtilClient.empty(err.message):
            # err 中含有 code 和 message 属性，可帮助开发定位问题
            print(err.code)
            print(err.message)



def get_media_id():
    access_token = getAccess_token()  # 拿到接口凭证
    path = './helloworld.txt'  # 文件地址
    url = 'https://oapi.dingtalk.com/media/upload?access_token=%s&type=file' % access_token
    files = {'media': open(path, 'rb')}
    data = {'access_token': access_token,
            'type': 'file'}
    response = requests.post(url, files=files, data=data)
    json = response.json()
    return json["media_id"]


def SendFile():
    access_token = getAccess_token()
    media_id = getMedia_id()
    chatid = '****'  # 通过jsapi工具获取的群聊id
    url = 'https://oapi.dingtalk.com/chat/send?access_token=' + access_token
    header = {
        'Content-Type': 'application/json'
    }
    data = {'access_token': access_token,
            'chatid': chatid,
            'msg': {
                'msgtype': 'file',
                'file': {'media_id': media_id}
            }}
    r = requests.request('POST', url, data=json.dumps(data), headers=header)
    print(r.json())


print(get_access_token())


