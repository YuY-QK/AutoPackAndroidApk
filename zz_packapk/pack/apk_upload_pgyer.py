#!/usr/bin/env python3
# encoding = utf-8
import os
import sys
import requests

requests.packages.urllib3.disable_warnings()

# 清空临时资源
def cleanTempResource(apkLogPath):
    try:
        os.remove(apkLogPath)
        pass
    except Exception:
        pass

def upload2pgyer():
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
        uKey = sys.argv[5]  # pgyer uKey
        _api_key = sys.argv[6]  # pgyer _api_key
        apklogo = sys.argv[7]  # 等待上传的APK logo路径
        apkpath = sys.argv[8]  # 等待上传的APK路径
        changelogtitle = sys.argv[9]  # 等待上传的APK更新日志标题
        apklogpath = sys.argv[10]  # 等待上传的APK更新日志文件地址
        print(
            f'appname:{appname}\n'
            f'apppackage:{apppackage}\n'
            f'appversion:{appversion}\n'
            f'appbuild:{appbuild}\n'
            f'uKey:{uKey}\n'
            f'_api_key:{_api_key}\n'
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

        # ============ 第一步：上传APK
        try:
            print("*********** uploading apk......")
            url = "https://www.pgyer.com/apiv2/app/upload"
            apkfile = {'file': open(apkpath, 'rb')}
            param = {
                #"uKey": uKey,
                "_api_key": _api_key,
                "installType": "1",
                "buildUpdateDescription": (changelogtitle + "\n" + changeLogInfo)
            }
            req = requests.post(
                url = url,
                files = apkfile,
                data = param,
                verify = False)
        except Exception as e:
            print("*********** upload apk error ***********")
            e.print_exc()

        download_url = 'https://www.pgyer.com/'
        if req.status_code == 200 :
            update_url = download_url + req.json()["data"]["buildShortcutUrl"]
            update_url_QRCode = req.json()["data"]["buildQRCodeURL"]
            build_version_no = req.json()["data"]["buildBuildVersion"]

            print("upload apk success, update url is " + update_url
                  + "\nappQRCodeUrl is " + update_url_QRCode
                  + "\nbuild_version_no is " + build_version_no
                  )
        else:
            print("*********** get upload apk info error ***********")


        # ============ 第二步：将APK信息写入文件【临时文件，用于发送消息】
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
            logFile.write('\n')
            logFile.write('QRCODE_URL=' + update_url_QRCode)
            logFile.write('\n')
            logFile.write('BUILD_VERSION=' + build_version_no)

if __name__ == '__main__':
    upload2pgyer()
