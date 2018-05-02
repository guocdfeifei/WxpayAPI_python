# 回调基础类
import WxpayAPI_python.Api
import WxpayAPI_python.Data as Data

WxpayApi = WxpayAPI_python.Api.WxPayApi


class WxPayNotify(Data.WxPayNotifyReply):

    def Handle(self, needSign=True, xml=""):
        """
        回调入口
        @param needSign bool  是否需要签名输出

        修改:
        -----
        1. 添加 xml 参数,即响应的 xml 字符串
        """
        # 当返回False的时候，表示notify中调用NotifyCallBack回调失败获取签名校验失败，此时直接回复失败
        result = WxpayApi.notify(self.NotifyCallBack, xml)  # 改为使用字典返回原先的 bool 和 msg
        if result["status"] is False:
            self.SetReturn_code("FAIL")
            self.SetReturn_msg(result["msg"])
            self.ReplyNotify(False)
            return
        else:
            # 该分支在成功回调到NotifyCallBack方法，处理完成之后流程
            self.SetReturn_code("SUCCESS")
            self.SetReturn_msg("OK")
        self.ReplyNotify(needSign)

    def NotifyProcess(self, data):
        """
        回调方法入口，子类可重写该方法
        注意：
        1、微信回调超时时间为2s，建议用户使用异步处理流程，确认成功之后立刻回复微信服务器
        2、微信服务器在调用失败或者接到回包为非确认包的时候，会发起重试，需确保你的回调是可以重入
        @param data array 回调解释出的参数
        @param msg string 如果回调处理失败，可以将错误信息输出到该方法
        @return True回调出来完成不需要继续回调，False回调处理未完成需要继续回调

        修改:
        -----
        去掉指针传参的 msg,修改返回值类型,
        返回值需要和 Api.notify 一致,改为返回字典,status 为原 bool,msg 用于原指针传参::
        {"status": False, "msg": ""}
        """
        return {"status": True, "msg": ""}
        # TODO 用户基础该类之后需要重写该方法，成功的时候返回True，失败返回False
        # return True

    def NotifyCallBack(self, data):
        """
        notify回调方法，该方法中需要赋值需要输出的参数,不可重写
        @param data array
        @return True回调出来完成不需要继续回调，False回调处理未完成需要继续回调

        修改:
        -----
        NotifyProcess 的返回值需要和 Api.notify 一致
        """
        msg = "OK"  #
        result = self.NotifyProcess(data)
        if result["status"] is True: # 修改 返回值需要和 Api.notify 一致
            self.SetReturn_code("SUCCESS")
            self.SetReturn_msg("OK")
        else:
            self.SetReturn_code("FAIL")
            self.SetReturn_msg(msg)
        return result

    def ReplyNotify(self, needSign=True):
        """
        回复通知
        @param needSign bool 是否需要签名输出
        """
        # 如果需要签名
        if needSign is True and self.GetReturn_code() == "SUCCESS":  # return_code 是哪来的? php版本可能有误
            self.SetSign()
        WxpayApi.replyNotify(self.ToXml())
