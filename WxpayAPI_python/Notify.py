# 回调基础类
import WxpayAPI_python.Api 
import WxpayAPI_python.Data as Data

WxpayApi = WxpayAPI_python.Api.WxPayApi

class WxPayNotify (Data.WxPayNotifyReply):
    
     # 回调入口
     # @param bool needSign  是否需要签名输出
    def  Handle(self, needSign = True):
    
        # 当返回False的时候，表示notify中调用NotifyCallBack回调失败获取签名校验失败，此时直接回复失败
        result = WxpayApi.notify(self.NotifyCallBack, msg)  # todo msg
        if result is False:
            self.SetReturn_code("FAIL")
            self.SetReturn_msg(msg)
            self.ReplyNotify(False)
            return
        else :
            # 该分支在成功回调到NotifyCallBack方法，处理完成之后流程
            self.SetReturn_code("SUCCESS")
            self.SetReturn_msg("OK")
        
        self.ReplyNotify(needSign)
    
    
    
     # 
     # 回调方法入口，子类可重写该方法
     # 注意：
     # 1、微信回调超时时间为2s，建议用户使用异步处理流程，确认成功之后立刻回复微信服务器
     # 2、微信服务器在调用失败或者接到回包为非确认包的时候，会发起重试，需确保你的回调是可以重入
     # @param array data 回调解释出的参数
     # @param string msg 如果回调处理失败，可以将错误信息输出到该方法
     # @return True回调出来完成不需要继续回调，False回调处理未完成需要继续回调
     #/
    def NotifyProcess(self, data, msg):
    
        # TODO 用户基础该类之后需要重写该方法，成功的时候返回True，失败返回False
        return True
    
    
    
     # 
     # notify回调方法，该方法中需要赋值需要输出的参数,不可重写
     # @param array data
     # @return True回调出来完成不需要继续回调，False回调处理未完成需要继续回调
     #/
    def  NotifyCallBack(self, data):
    
        msg = "OK"  # todo  msg 应该都是用的这个
        result = self.NotifyProcess(data, msg)
        
        if result is True :
            self.SetReturn_code("SUCCESS")
            self.SetReturn_msg("OK")
        else :
            self.SetReturn_code("FAIL")
            self.SetReturn_msg(msg)
        
        return result
    
    
    
     # 
     # 回复通知
     # @param bool needSign 是否需要签名输出
    def ReplyNotify(self, needSign = True):
    
        # 如果需要签名
        if(needSign == True  and            self.GetReturn_code(return_code) == "SUCCESS"):
        
            self.SetSign()
        
        WxpayApi.replyNotify(self.ToXml())
    
