#!/usr/bin/python
# -*- coding: UTF-8 -*-
'''
author:suzhenjing
data:18-9-30
功能:
'''

# !/usr/bin/python
# -*- coding: UTF-8 -*-
'''
author:suzhenjing
data:18-9-30
功能:
'''
import json
import copy
import random
import base64
import binascii
import requests
import sys
from Crypto.Cipher import AES
from Crypto.PublicKey import RSA

reload(sys)
sys.setdefaultencoding('utf8')

# 实现函数a，生成16位的随机字符，生成16位的随机字符
def random_b():
    seed = "1234567890abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    sa = []
    for i in range(16):
        sa.append(random.choice(seed))
    salt = ''.join(sa)
    return bytes(salt)


# e rsa公钥组成
pub_key = '010001'
# f rsa公钥组成
moudules = "00e0b509f6259df8642dbc35662901477df22677ec152b5ff68ace615bb7b725152b3ab17a876aea8a5aa76d2e417629ec4ee341f56135fccf695280104e0312ecbda92557c93870114af6c9d05c4f7f0c3685b7a46bee255932575cce10b424d813cfe4875d3e82047b97ddef52741d546b8e289dc6935b3ece0462db0a22b8e7"
# g aes密钥
secret_key = b'0CoJUm6Qyw8W8jud'

"""
AES 加密
"""


def aes_encrypt(text, key):
    iv = b'0102030405060708'
    # 对长度不是16倍数的字符串进行补全，再转为bytes数据
    pad = 16 - len(text) % 16
    try:
        # 如果接到bytes数据（如第一次aes加密得到的密文）要解码再进行补全
        text = text.decode()
    except:
        pass

    text = text + pad * chr(pad)
    try:
        text = text.encode()
    except:
        pass

    # key密钥加上偏移量形成新的密钥
    encryptor = AES.new(key, AES.MODE_CBC, iv)
    # 对text加密
    ciphertext = encryptor.encrypt(text)
    # 得到的秘闻还要继续base64编码
    ciphertext = base64.b64encode(ciphertext).decode('utf-8')
    return ciphertext


"""
RSA加密
"""


def rsa_encrypt(random_char):
    # 明文处理，反序并hex编码
    text = random_char[::-1]
    rsa = int(binascii.hexlify(text), 16) ** int(pub_key, 16) % int(moudules, 16)
    return format(rsa, 'x').zfill(256)


"""
构造params
"""


def aes_param(data):
    text = json.dumps(data)
    random_char = random_b()
    params = aes_encrypt(text, secret_key)
    params = aes_encrypt(params, random_char)
    enc_sec_key = rsa_encrypt(random_char)
    data = {
        'params': params,
        'encSecKey': enc_sec_key
    }
    return data


"""
请求头
"""
headers = {
    'Connection': 'keep-alive',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36',
    'Host': 'music.163.com',
    'Origin': 'https://music.163.com',
}

"""
通过歌曲id爬取歌词内容
"""

if __name__ == '__main__':
    # 搜索歌词url
    query_url = 'https://music.163.com/weapi/cloudsearch/get/web?csrf_token='
    data = {"hlpretag": "<span class=\"s-fc7\">",
            "hlposttag": "</span>",
            "s": "中国新说唱",
            "type": "1",
            "offset": "0",
            "total": "true",
            "limit": "30",
            "csrf_token": ""
            }
    data = aes_param(data)
    referer = 'https://music.163.com/search/'
    headers['referer'] = referer
    result = requests.post(query_url, data=data, headers=headers)
    result = result.json()
    songs = result['result']['songs']
    for song in songs:
        dict = {}
        dict['name'] = song['name']
        dict['id'] = song['id']
        dict_up = copy.deepcopy(dict)
        dict_up_json = json.dumps(dict_up, ensure_ascii=False)
        with open('wangyiyun.json','a') as f:
            f.write(dict_up_json + ',\n')