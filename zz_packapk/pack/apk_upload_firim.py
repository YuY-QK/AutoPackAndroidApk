#!/usr/bin/env python3
# encoding = utf-8
import os
import sys
import traceback
import requests

requests.packages.urllib3.disable_warnings()

# 清空临时资源
def cleanTempResource(apkLogPath):
    try:
        os.remove(apkLogPath)
        pass
    except Exception:
        pass

def upload2fir():
    # 参数检查
    paramNum = 10
    sysLen = len(sys.argv)
    if sysLen < paramNum:
        print("*********** PARAM IS ERROR *********** ")
        return
    else:
        # 基础参数
        appname = sys.argv[1]  # app名称
        apppackage = sys.argv[2]  # 唯一包名，也即是bundle_id
        appversion = sys.argv[3]  # app版本号
        appbuild = sys.argv[4]  # app build号
        appid = sys.argv[5]  # fir appid
        apitoken = sys.argv[6]  # fir token
        apklogo = sys.argv[7]  # 等待上传的APK logo路径
        apkpath = sys.argv[8]  # 等待上传的APK路径
        changelogtitle = sys.argv[9]  # 等待上传的APK更新日志标题
        apklogpath = sys.argv[10]  # 等待上传的APK更新日志文件地址
        print(
            f'appname:{appname}\n'
            f'apppackage:{apppackage}\n'
            f'appversion:{appversion}\n'
            f'appbuild:{appbuild}\n'
            f'apitoken:{apitoken}\n'
            f'appid:{appid}\n'
            f'apklogo:{apklogo}\n'
            f'apkpath:{apkpath}\n'
            f'changelogtitle:{changelogtitle}\n'
            f'apkchangelog:{apklogpath}')

        changeLogInfo = ""
        ### 读取信息
        with open(apklogpath, 'r+') as logFile:
            lines = logFile.readlines()
            for i in range(0, len(lines)):
                if lines[i].startswith("#"):
                    continue
                else:
                    changeLogInfo += lines[i]

        # ============ 第一步：获取fir上传凭证
        print("get fir upload certificate")
        icondict = {}  # 后面上传图标和apk需要使用的参数，这里保存下来
        binarydict = {}
        try:
            req = requests.post(
                "http://api.bq04.com/apps",
                {
                    'type': 'android',
                    'bundle_id': apppackage,
                    'api_token': apitoken
                })
            resjson = req.json()
            icondict = (resjson["cert"]["icon"])
            binarydict = (resjson["cert"]["binary"])
            print("*********** get fir upload certificate success ***********")

        except Exception as e:
            print("*********** get fir upload certificate error ***********")
            e.print_exc()

        # ============ 第二步：上传APK
        try:
            print("*********** uploading apk......")
            apkfile = {'file': open(apkpath, 'rb')}
            param = {
                "key": binarydict["key"],
                "token": binarydict["token"],
                "x:name": appname,
                "x:version": appversion,
                "x:build": appbuild,
                "x:changelog": (changelogtitle + "\n" + changeLogInfo)
            }
            req = requests.post(
               url = binarydict["upload_url"],
               files = apkfile,
               data = param,
               verify = False)
        except Exception as e:
            print("*********** upload apk error ***********")
            e.print_exc()

        # ============ 第三步：上传APK logo
        try:
            apklogofile = {'file': open(apklogo, 'rb')}
            param = {
                "key": icondict["key"],
                "token": icondict["token"]
            }
            req = requests.post(
                url = icondict["upload_url"],
                files = apklogofile,
                data = param,
                verify = False)
        except Exception:
            print("*********** upload apk logo error ***********")
            traceback.print_exc()

        # ============ 第四步：获取APK最新下载地址
        queryurl = 'http://api.bq04.com/apps/latest/%s?api_token=%s' % (appid, apitoken)
        update_url = ""
        try:
            req = requests.get(queryurl)
            update_url = (req.json()["update_url"])
            print("upload apk success, update url is " + update_url)
        except Exception:
            print("*********** get apk down url error ***********")
            traceback.print_exc()

        # ============ 第五步：将APK信息写入文件
        apklofile = apklogpath + "_" + appbuild
        cleanTempResource(apklofile)
        with open(apklofile, 'w+') as logFile:
            logFile.write('\n')
            logFile.write('TITLE=' + changelogtitle)
            logFile.write('\n')
            logFile.write('VERSION_NAME=' + appversion)
            logFile.write('\n')
            logFile.write('VERSION_CODE=' + appbuild)
            logFile.write('\n')
            logFile.write('CHANGE_LOG=' + changeLogInfo.replace("\n", "[n]"))
            logFile.write('\n')
            logFile.write('UPDATE_URL=' + update_url)

if __name__ == '__main__':
    upload2fir()
