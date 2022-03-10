#!/usr/bin/env python3
# encoding = utf-8
import os
import sys
import requests

from io import BytesIO
import base64
import hashlib

requests.packages.urllib3.disable_warnings()

# 清空临时资源
def cleanTempResource(apkLogPath):
    try:
        os.remove(apkLogPath)
        pass
    except Exception:
        pass

def pushMsg():
    sysLen = len(sys.argv)
    if sysLen < 1:
        print("*********** PARAM IS ERROR *********** ")
        return
    pushkey = sys.argv[1]
    apklogFile = sys.argv[2]
    testPhone = sys.argv[3]
    picker = sys.argv[4]

    log_title = ""
    version_name = ""
    version_code = ""
    change_log = ""
    update_url = ""
    qrcode_url = ""

    ### 读取信息
    with open(apklogFile, 'r+') as logFile:
        lines = logFile.readlines()
        for i in range(0, len(lines)):
            if lines[i].startswith("TITLE="):
                log_title = lines[i].replace("TITLE=", "")
            if lines[i].startswith("VERSION_NAME="):
                version_name = lines[i].strip('\n').replace("VERSION_NAME=", "")
            if lines[i].startswith("VERSION_CODE="):
                version_code = lines[i].strip('\n').replace("VERSION_CODE=", "")
            if lines[i].startswith("CHANGE_LOG="):
                change_log = lines[i].strip('\n').replace("CHANGE_LOG=", "").replace("[n]", "\n")
            if lines[i].startswith("UPDATE_URL="):
                update_url = lines[i].strip('\n').replace("UPDATE_URL=", "")
            if lines[i].startswith("QRCODE_URL="):
                qrcode_url = lines[i].strip('\n').replace("QRCODE_URL=", "")
            if lines[i].startswith("BUILD_VERSION="):
                build_version = lines[i].strip('\n').replace("BUILD_VERSION=", "")

    phones = testPhone.split("-")

    headers = {"Content-Type": "application/json"}
    content = log_title + \
              "[版本: " + version_name + " (Code:" + version_code + " | Build: " + build_version + ")](" + update_url + ")\n" + \
              picker + "\n" + change_log
    # 图片保存在内存
    response = requests.get(qrcode_url)
    buff = BytesIO(response.content).read()
    # 得到图片的base64编码
    base64_str = str(base64.b64encode(buff), encoding='utf-8')
    picMd5 = str(hashlib.md5(buff).hexdigest())

    #通知所有人
    data2people = {
        "msgtype": "text",
        "text": {
            "mentioned_mobile_list": phones
        }
    }
    # 文本数据
    textData = {
        "msgtype": "markdown",
        "markdown": {
            "content": content,
        }
    }
    # 图片数据
    picData = {
        "msgtype": "image",
        "image": {
            "base64": base64_str,
            "md5": picMd5
        }
    }
    try:
        r = requests.post(
            url='https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key='+ pushkey,
            headers=headers,
            json=data2people)
        r = requests.post(
            url='https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key='+ pushkey,
            headers=headers,
            json=textData)
        r = requests.post(
            url='https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key='+ pushkey,
            headers=headers,
            json=picData)
    except Exception as e:
        print("error pushmsg")

    cleanTempResource(apklogFile)

if __name__ == '__main__':
    pushMsg()
