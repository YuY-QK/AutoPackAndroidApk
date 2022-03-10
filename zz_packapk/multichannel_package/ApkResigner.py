#!/usr/bin/python  
#-*-coding:utf-8-*-

# /**
#  * ================================================
#  * 作    者：JayGoo
#  * 版    本：1.0.1
#  * 更新日期：2017/12/29
#  * 邮    箱: 1015121748@qq.com
#  * ================================================
#  */

import os
import sys
import config
import platform

#渠道包输出目录
channelsOutputFilePath = ""
#当前脚本文件所在目录
parentPath = ""

#获取脚本文件的当前路径
def curFileDir():
    #获取脚本路径
    path = sys.path[0]
    #判断为脚本文件还是py2exe编译后的文件，
    #如果是脚本文件，则返回的是脚本的目录，
    #如果是编译后的文件，则返回的是编译后的文件路径
    if os.path.isdir(path):
        return path
    elif os.path.isfile(path):
        return os.path.dirname(path)

#判断当前系统
def isWindows():
    sysstr = platform.system()
    if("Windows" in sysstr):
        return 1
    else:
        return 0

#兼容不同系统的路径分隔符
def getBackslash():
    if(isWindows() == 1):
        return "\\"
    else:
        return "/"


# 清空临时资源
def cleanTempResource(zipalignedApkPath, signedApkPath):
    try:
        os.remove(zipalignedApkPath)
        os.remove(signedApkPath)
        pass
    except Exception:
        pass

# 创建Channels输出文件夹
def createChannelsDir(channelsOutputFilePath):
    try:
        os.makedirs(channelsOutputFilePath)
        pass
    except Exception:
        print(channelsOutputFilePath)
        print('创建文件夹失败')
        pass


#重新签名apk
#python3 ApkResigner.py keystorePath keyAlias keystorePassword keyPassword
def reSigneApk():
    # 参数检查
    paramNum = 5
    sysLen = len(sys.argv)
    if sysLen < paramNum:
        print("please input param")
        return

    #config
    parentPath = curFileDir() + getBackslash()
    libPath = parentPath + "lib" + getBackslash()
    sdkBuildToolPath = sys.argv[5]
    #不使用config里的sdkBuildToolPath，用传入的
    buildToolsPath = sdkBuildToolPath + getBackslash()
    checkAndroidV2SignaturePath = libPath + "CheckAndroidV2Signature.jar"
    walleChannelWritterPath = libPath + "walle-cli-all.jar"
    channelsOutputFilePath = parentPath + "channels"
    channelFilePath = parentPath + "channel"
    protectedSourceApkPath = parentPath + config.protectedSourceApkName

    # keystorePath = config.keystorePath
    # keyAlias = config.keyAlias
    # keystorePassword = config.keystorePassword
    # keyPassword = config.keyPassword
    keystorePath = sys.argv[1]
    keyAlias = sys.argv[2]
    keystorePassword = sys.argv[3]
    keyPassword = sys.argv[4]
    print(f'keystorePath:{keystorePath}\n'
          f'keyAlias:{keyAlias}\n'
          f'keystorePassword:{keystorePassword}\n'
          f'keyPassword:{keyPassword}')

    # 检查自定义路径，并作替换
    if len(config.protectedSourceApkDirPath) > 0:
        protectedSourceApkPath = config.protectedSourceApkDirPath + getBackslash() + config.protectedSourceApkName

    if len(config.channelsOutputFilePath) > 0:
        channelsOutputFilePath = config.channelsOutputFilePath

    if len(config.channelFilePath) > 0:
        channelFilePath = config.channelFilePath

    zipalignedApkPath = protectedSourceApkPath[0 : -4] + "_aligned.apk"
    signedApkPath = zipalignedApkPath[0 : -4] + "_signed.apk"

    # 创建Channels输出文件夹
    createChannelsDir(channelsOutputFilePath)

    #对齐
    zipalignShell = buildToolsPath + "zipalign -v 4 " + protectedSourceApkPath + " " + zipalignedApkPath
    os.system(zipalignShell)

    #签名
    signShell = buildToolsPath + "apksigner sign --ks "+ keystorePath + " --ks-key-alias " + keyAlias + " --ks-pass pass:" + keystorePassword + " --key-pass pass:" + keyPassword + " --out " + signedApkPath + " " + zipalignedApkPath
    os.system(signShell)
    print(signShell)

    #检查V2签名是否正确
    checkV2Shell = "java -jar " + checkAndroidV2SignaturePath + " " + signedApkPath
    os.system(checkV2Shell)

    #写入渠道
    if len(config.extraChannelFilePath) > 0:
        writeChannelShell = "java -jar " + walleChannelWritterPath + " batch2 -f " + config.extraChannelFilePath + " " + signedApkPath + " " + channelsOutputFilePath
    else:
        writeChannelShell = "java -jar " + walleChannelWritterPath + " batch -f " + channelFilePath + " " + signedApkPath + " " + channelsOutputFilePath

    os.system(writeChannelShell)

    cleanTempResource(zipalignedApkPath, signedApkPath)

    print("\n↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓   Please check channels in the path   ↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓")
    print("\n" + channelsOutputFilePath)
    print("\n**** =============================TASK FINISHED=================================== ****\n")

if __name__ == '__main__':
    reSigneApk()
