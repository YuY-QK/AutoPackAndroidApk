#!/usr/bin/env python3
# encoding = utf-8
import sys
import requests

requests.packages.urllib3.disable_warnings()

def pushChannelMsg():
    sysLen = len(sys.argv)
    if sysLen < 1:
        print("*********** PARAM IS ERROR *********** ")
        return
    pushkey = sys.argv[1]
    testPhone = sys.argv[2]
    content = sys.argv[3]
    appName = sys.argv[4]
    versionName = sys.argv[5]
    versionCode = sys.argv[6]
    apklogpath = sys.argv[7]
    packApkUser = sys.argv[8]

    logPreInfo = content + "\n\n" + appName + "APP" + versionName + "(" + versionCode + ")\n" + \
                 packApkUser + "\n"

    changeLogInfo = ""
    ### 读取信息
    with open(apklogpath, 'r+') as logFile:
        lines = logFile.readlines()
        for i in range(0, len(lines)):
            if lines[i].startswith("#"):
                continue
            else:
                changeLogInfo += lines[i]

    apkLogInfo = logPreInfo + changeLogInfo

    phones = testPhone.split("-")

    headers = {"Content-Type": "application/json"}
    data = {
        "msgtype": "text",
        "text": {
            "content": apkLogInfo,
            "mentioned_mobile_list": phones
        }
    }
    try:
        r = requests.post(
            url='https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key='+ pushkey,
            headers=headers,
            json=data)
    except Exception as e:
        print("error pushmsg")


if __name__ == '__main__':
    pushChannelMsg()
