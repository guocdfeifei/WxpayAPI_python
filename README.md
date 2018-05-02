# WxpayAPI_python
基于腾讯官方 WxpayAPI_php_v3.0.1 翻译 python 版本

**注意,翻译尚未完成** 

**欢迎参与翻译** **欢迎 star** **欢迎 fork**

## 缘由:
* 我热爱 python
* 官方提供 php ,二没有python 版本
* php 和 python 都是动态类型语言
* php 转换为 python 相对比较容易

# 目标
* 基本按 php 版本的结构逐行进行翻译,尽量少修改代码结构,便于同步更新 php 版本
* 方法和变量名保持不变
* 除特别的地方外,用法几乎和官方的一样
* 做成有通用意义的 python 模块,不依赖特定 web 框架

# 感谢
* www.php2python.com 提供了大量的 php 转python 的函数,简化了很多工作

## 翻译原则
* 基本语法
* 替换可直接替代的函数
* 不能直接替代的手写一个 python 版的同功能函数

## 区别
* Api.WxPayApi:
    * 使用时先初始化,该类,并传 ip,替换 php 版本用使用 _SERVER 直接获取 ip
* Data.WxPayNotify.Handle 方法添加了一个 xml 参数,需要自己获取返回的xml内容传参
* Data.WxPayNotify.NotifyProcess 去掉了 msg 参数,具体实现的返回值 和 Api.notify 一样
* Api.WxPayApi.notify 
    * 参数:
        * 去掉了指针传参的 msg,改为返回 msg字符串,并因此改变了原返回值类型
        * 添加了一个 xml 参数,即原先使用 file_get_contents('php://input') 获取的响应,便于任何 web 框架传参
    * 返回值:
        * 返回值修改为字典 {"status": False, "msg": e.errorMessage()}
        * 键 status 为原先返回的 bool
        * 键 msg 为原先使用指针传递的 msg
* Api.WxPayApi.replyNotify 在 php 版本中仅仅是输出字符串,可直接替换为 web 框架的输出语句    
    
# 建议
* 开发环境为 python3,代码里有一些适配 pyhton2 的语句,但还有很多地方不支持 python2    
* 在每次请求中都初始化一次所有的类比较好,避免出错
* Config.WxPayConfig
    * 建议使用新加的 init_with_dict 方法替换该方法的属性值,主要是证书路径一定写好        
    

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
* Data.FromXml.WxPayDataBase.simplexml_load_string 要根据返回的数据再分析如何解析
    * Util.simplexml_load_string
