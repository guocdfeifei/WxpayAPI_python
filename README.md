# WxpayAPI_python
基于腾讯官方 WxpayAPI_php_v3.0.1 翻译为 python 版本

**注意,翻译尚未完成**

## 缘由:
* 我热爱 python
* 官方提供 php ,二没有python 版本
* php 和 python 都是动态类型语言
* php 转换为 python 相对比较容易

# 目标
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

# TODO
* Data 基本翻译完, simplexml_load_string实属的实现
* 还有几个 new self() 等的地方没改
* 直接使用 msg 指针的几个地方
* 使用 file_get_contents 
* return_code
* 证书路径