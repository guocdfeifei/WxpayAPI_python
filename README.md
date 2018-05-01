# WxpayAPI_python
基于腾讯官方 WxpayAPI_php_v3.0.1 翻译为 python 版本

**注意,翻译尚未完成**

## 缘由:
* 我热爱 python
* 官方提供 php ,二没有python 版本
* php 和 python 都是动态类型语言
* php 转换为 python 相对比较容易

# 目标
* 基本按 php 版本的结构逐行进行翻译,尽量少修改代码结构,亿便于同步更新 php 版本
* 做成有通用意义的 python 模块,不依赖特定 web 框架

# 感谢
* www.php2python.com 提供了大量的 php 转python 的函数,简化了很多工作

## 翻译原则
* 基本语法
* 替换可直接替代的函数
* 不能直接替代的手写一个 python 版的同功能函数

## 区别
* php 版本用使用 _SERVER 直接获取参数的地方要改为传参
* php 版本原来有直接 echo 的要改为返回

# 进度
* [*]复制文件结构
* [*]语法翻译
* [ ]实现逻辑,目前有些没完成
* [ ]测试

# 问题:
    * 由于注释太多,没有全部改为 python 标准的 docstring 形式
    * 可能 php 版也存在的问题:
        * NOTIFY_URL 和 return_code 找不到

# TODO
* simplexml_load_string 实属的实现
* 几个 new self() 等的地方 待测试
* 直接使用 msg 指针的几个地方
* 使用 file_get_contents 
* 证书路径
