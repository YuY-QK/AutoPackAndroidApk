# AutoPackAndroidApk
android项目自动打包，解放一只手


# 项目使用说明：
自动化编译、打包、上传、推送等集成方式

## 1、文件组成：

- apk_channgelog        ：更新日志

### 上传fir.im / pgyer：
- apk_upload.gradle     ：上传到fir.im / pgyer的任务
- apk_upload_firim.py   ：上传fir.im / pgyer工具python
- apk_upload_pyger.py   ：上传pgyer工具python
- apk_upload_wxpush_code.py    ：上传后发送消息通知python【蒲公英用，有二维码图片】
- apk_upload_wxpush.py         ：上传后发送消息通知python【fir用】

### 360加固
- apk_firm.gradle       ：加固任务【加固账号密码在其中配置的】
- jiagu360              ：目录，360官网加固下载的工具包

### 渠道包
- apk_channel.gradle    ：生成渠道包任务
- apk_channel_wxpush.py ：渠道包生成消息通知python
- multichannel_pachage  ：目录，生成渠道包工具
-- 加固包在此目录下【名为`app-release.apk`】

## 2、相关配置说明：
### a. 更新日志：
- 每次开发或修改bug的日志，可在`apk_channgelog`中编辑

### b. key相关配置【**重点**】：
- 配置的参数在`app/gradle.properties`此文件中，具体参数说明请看此文件
  相关配置都要在这个文件中进行修改配置

## 3、使用说明：
### a. 任务Task
- 所有生成的`Task`任务，都在`gradle`标签下的`apk_pack`任务组中
- 相关任务都是基于`assemble<buildType>`(如生产为`assembleRelease`)的
    若要基于微信混淆打包`andreguard`进行二次处理，
    需要修改`apk_config.gradle`中的`TASK_DEPEND = "andreguard"`

### b. 使用方式：
- 发布上线前：
    执行`apk_pack`下的`apkUpload_Xxx`的任务，进行不同环境下的编译打包，并上传推送
- 发布上线时：
    执行`apk_pack`下的`apkChannel_Xxx`的任务，生成相应的各个渠道包，
    在`multichannel_pachage/channels`目录下，并推送消息于企业微信群中



