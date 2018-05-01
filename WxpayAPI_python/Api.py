# from Exception import *
# from  Config import *
# from Data  import *

import WxpayAPI_python.Exception
import WxpayAPI_python.Config
import WxpayAPI_python.Data
# import WxpayAPI_python.Data.WxPayResults as WxPayResults

WxPayException = WxpayAPI_python.Exception.WxPayException
WxPayConfig = WxpayAPI_python.Config.WxPayConfig
WxPayResults = WxpayAPI_python.Data.WxPayResults

from WxpayAPI_python.Util import *  # 导入 php 的同名同功能函数




class WxPayApi():
    """
    接口访问类，包含所有微信支付API列表的封装，类中方法为static方法，
    每个接口有默认超时时间（除提交被扫支付为10s，上报超时时间为1s外，其他均为6s）
     """
    def unifiedOrder(self ,inputObj, timeOut = 6):
        """
        统一下单，WxPayUnifiedOrder中out_trade_no、body、total_fee、trade_type必填
        appid、mchid、spbill_create_ip、nonce_str不需要填入
        """
        url = "https://#api.mch.weixin.qq.com/pay/unifiedorder"
        # 检测必填参数
        if (not inputObj.IsOut_trade_noSet()) :
            raise WxPayException("缺少统一支付接口必填参数out_trade_no！")
        elif (not inputObj.IsBodySet()):
            raise WxPayException("缺少统一支付接口必填参数body！")
        elif (not inputObj.IsTotal_feeSet()):
            raise WxPayException("缺少统一支付接口必填参数total_fee！")
        elif (not inputObj.IsTrade_typeSet()):
            raise WxPayException("缺少统一支付接口必填参数trade_type！")

        # 关联参数
        if (inputObj.GetTrade_type() == "JSAPI" and  not inputObj.IsOpenidSet()):
            raise WxPayException("统一支付接口中，缺少必填参数openid！trade_type为JSAPI时，openid为必填参数！")
        
        if (inputObj.GetTrade_type() == "NATIVE" and  not inputObj.IsProduct_idSet()):
            raise WxPayException("统一支付接口中，缺少必填参数product_id！trade_type为JSAPI时，product_id为必填参数！")
        

        # 异步通知url未设置，则使用配置文件中的url
        if (not inputObj.IsNotify_urlSet()):
            inputObj.SetNotify_url(WxPayConfig.NOTIFY_URL) # 异步通知url
        

        inputObj.SetAppid(WxPayConfig.APPID) # 公众账号ID
        inputObj.SetMch_id(WxPayConfig.MCHID) # 商户号
        # inputObj.SetSpbill_create_ip(_SERVER['REMOTE_ADDR']) # 终端ip    todo
                                                                    #inputObj.SetSpbill_create_ip("1.1.1.1")
        inputObj.SetNonce_str(self.getNonceStr()) # 随机字符串

        # 签名
        inputObj.SetSign()
        xml = inputObj.ToXml()

        startTimeStamp = self.getMillisecond() # 请求开始时间
        response = self.postXmlCurl(xml, url, False, timeOut)
        result = WxPayResults.Init(response)
        self.reportCostTime(url, startTimeStamp, result) # 上报请求花费时间

        return result

    def orderQuery(self, inputObj, timeOut = 6):
        """
        查询订单，WxPayOrderQuery中out_trade_no、transaction_id至少填一个
        appid、mchid、spbill_create_ip、nonce_str不需要填入
        @param WxPayOrderQuery inputObj
        @param int timeOut
        @throws WxPayException
        @return 成功时返回，其他抛异常
        """
	
        url = "https:#api.mch.weixin.qq.com/pay/orderquery"
        # 检测必填参数
        if not inputObj.IsOut_trade_noSet() and  not inputObj.IsTransaction_idSet():
            raise WxPayException("订单查询接口中，out_trade_no、transaction_id至少填一个！")
		
        inputObj.SetAppid(WxPayConfig.APPID)#公众账号ID
        inputObj.SetMch_id(WxPayConfig.MCHID)#商户号
        inputObj.SetNonce_str(self.getNonceStr())#随机字符串
		
        inputObj.SetSign()#签名
        xml = inputObj.ToXml()

        startTimeStamp = self.getMillisecond()#请求开始时间
        response = self.postXmlCurl(xml, url, False, timeOut)
        result = WxPayResults.Init(response)
        self.reportCostTime(url, startTimeStamp, result)#上报请求花费时间

        return result
	
	




    def closeOrder(self, inputObj, timeOut = 6):
        """
        关闭订单，WxPayCloseOrder中out_trade_no必填
        appid、mchid、spbill_create_ip、nonce_str不需要填入
        @param WxPayCloseOrder inputObj
        @param int timeOut
        @throws WxPayException
        @return 成功时返回，其他抛异常
        """

        url = "https:#api.mch.weixin.qq.com/pay/closeorder"
        #检测必填参数
        if not inputObj.IsOut_trade_noSet():
            raise WxPayException("订单查询接口中，out_trade_no必填！")

        inputObj.SetAppid(WxPayConfig.APPID)#公众账号ID
        inputObj.SetMch_id(WxPayConfig.MCHID)#商户号
        inputObj.SetNonce_str(self.getNonceStr())#随机字符串

        inputObj.SetSign()#签名
        xml = inputObj.ToXml()

        startTimeStamp = self.getMillisecond()#请求开始时间
        response = self.postXmlCurl(xml, url, False, timeOut)
        result = WxPayResults.Init(response)
        self.reportCostTime(url, startTimeStamp, result)#上报请求花费时间

        return result



    def refund(self, inputObj, timeOut = 6):
        """
          申请退款，WxPayRefund中out_trade_no、transaction_id至少填一个且
          out_refund_no、total_fee、refund_fee、op_user_id为必填参数
          appid、mchid、spbill_create_ip、nonce_str不需要填入
          @param WxPayRefund inputObj
          @param int timeOut
          @throws WxPayException
          @return 成功时返回，其他抛异常
        """

        url = "https:#api.mch.weixin.qq.com/secapi/pay/refund"
        #检测必填参数
        if not inputObj.IsOut_trade_noSet() and  not inputObj.IsTransaction_idSet():
            raise WxPayException("退款申请接口中，out_trade_no、transaction_id至少填一个！")
        elif not inputObj.IsOut_refund_noSet():
            raise WxPayException("退款申请接口中，缺少必填参数out_refund_no！")
        elif not inputObj.IsTotal_feeSet():
            raise WxPayException("退款申请接口中，缺少必填参数total_fee！")
        elif not inputObj.IsRefund_feeSet():
            raise WxPayException("退款申请接口中，缺少必填参数refund_fee！")
        elif not inputObj.IsOp_user_idSet():
            raise WxPayException("退款申请接口中，缺少必填参数op_user_id！")

        inputObj.SetAppid(WxPayConfig.APPID)#公众账号ID
        inputObj.SetMch_id(WxPayConfig.MCHID)#商户号
        inputObj.SetNonce_str(self.getNonceStr())#随机字符串

        inputObj.SetSign()#签名
        xml = inputObj.ToXml()
        startTimeStamp = self.getMillisecond()#请求开始时间
        response = self.postXmlCurl(xml, url, True, timeOut)
        result = WxPayResults.Init(response)
        self.reportCostTime(url, startTimeStamp, result)#上报请求花费时间

        return result



     #
     #  查询退款
     #  提交退款申请后，通过调用该接口查询退款状态。退款有一定延时，
     #  用零钱支付的退款20分钟内到账，银行卡支付的退款3个工作日后重新查询退款状态。
     #  WxPayRefundQuery中out_refund_no、out_trade_no、transaction_id、refund_id四个参数必填一个
     #  appid、mchid、spbill_create_ip、nonce_str不需要填入
     #  @param WxPayRefundQuery inputObj
     #  @param int timeOut
     #  @throws WxPayException
     #  @return 成功时返回，其他抛异常

    def refundQuery(self, inputObj, timeOut=6):

        url = "https:#api.mch.weixin.qq.com/pay/refundquery"
        # 检测必填参数
        if not inputObj.IsOut_refund_noSet() and \
                not inputObj.IsOut_trade_noSet() and \
                not inputObj.IsTransaction_idSet() and \
                not inputObj.IsRefund_idSet():
            raise WxPayException("退款查询接口中，out_refund_no、out_trade_no、transaction_id、refund_id四个参数必填一个！")

        inputObj.SetAppid(WxPayConfig.APPID)  # 公众账号ID
        inputObj.SetMch_id(WxPayConfig.MCHID)  # 商户号
        inputObj.SetNonce_str(self.getNonceStr())  # 随机字符串

        inputObj.SetSign()  # 签名
        xml = inputObj.ToXml()

        startTimeStamp = self.getMillisecond()  # 请求开始时间
        response = self.postXmlCurl(xml, url, False, timeOut)
        result = WxPayResults.Init(response)
        self.reportCostTime(url, startTimeStamp, result)  # 上报请求花费时间

        return result



     #  下载对账单，WxPayDownloadBill中bill_date为必填参数
     #  appid、mchid、spbill_create_ip、nonce_str不需要填入
     #  @param WxPayDownloadBill inputObj
     #  @param int timeOut
     #  @throws WxPayException
     #  @return 成功时返回，其他抛异常

    def downloadBill(self, inputObj, timeOut = 6):

        url = "https:#api.mch.weixin.qq.com/pay/downloadbill"
        #检测必填参数
        if not inputObj.IsBill_dateSet():
            raise WxPayException("对账单接口中，缺少必填参数bill_date！")

        inputObj.SetAppid(WxPayConfig.APPID)#公众账号ID
        inputObj.SetMch_id(WxPayConfig.MCHID)#商户号
        inputObj.SetNonce_str(self.getNonceStr())#随机字符串

        inputObj.SetSign()#签名
        xml = inputObj.ToXml()

        response = self.postXmlCurl(xml, url, False, timeOut)
        if substr(response, 0 , 5) == "<xml>":
            return ""

        return response



     #  提交被扫支付API
     #  收银员使用扫码设备读取微信用户刷卡授权码以后，二维码或条码信息传送至商户收银台，
     #  由商户收银台或者商户后台调用该接口发起支付。
     #  WxPayWxPayMicroPay中body、out_trade_no、total_fee、auth_code参数必填
     #  appid、mchid、spbill_create_ip、nonce_str不需要填入
     #  @param WxPayWxPayMicroPay inputObj
     #  @param int timeOut

    def micropay(self, inputObj, timeOut = 10):

        url = "https:#api.mch.weixin.qq.com/pay/micropay"
        #检测必填参数
        if not inputObj.IsBodySet():
            raise WxPayException("提交被扫支付API接口中，缺少必填参数body！")
        elif not inputObj.IsOut_trade_noSet():
            raise WxPayException("提交被扫支付API接口中，缺少必填参数out_trade_no！")
        elif not inputObj.IsTotal_feeSet():
            raise WxPayException("提交被扫支付API接口中，缺少必填参数total_fee！")
        elif not inputObj.IsAuth_codeSet():
            raise WxPayException("提交被扫支付API接口中，缺少必填参数auth_code！")


        # inputObj.SetSpbill_create_ip(_SERVER['REMOTE_ADDR'])#终端ip  todo
        inputObj.SetAppid(WxPayConfig.APPID)#公众账号ID
        inputObj.SetMch_id(WxPayConfig.MCHID)#商户号
        inputObj.SetNonce_str(self.getNonceStr())#随机字符串

        inputObj.SetSign()#签名
        xml = inputObj.ToXml()

        startTimeStamp = self.getMillisecond()#请求开始时间
        response = self.postXmlCurl(xml, url, False, timeOut)
        result = WxPayResults.Init(response)
        self.reportCostTime(url, startTimeStamp, result)#上报请求花费时间

        return result



     #
     #  撤销订单API接口，WxPayReverse中参数out_trade_no和transaction_id必须填写一个
     #  appid、mchid、spbill_create_ip、nonce_str不需要填入
     #  @param WxPayReverse inputObj
     #  @param int timeOut
     #  @throws WxPayException

    def reverse(self, inputObj, timeOut = 6):

        url = "https:#api.mch.weixin.qq.com/secapi/pay/reverse"
        #检测必填参数
        if not inputObj.IsOut_trade_noSet() and  not inputObj.IsTransaction_idSet():
            raise WxPayException("撤销订单API接口中，参数out_trade_no和transaction_id必须填写一个！")


        inputObj.SetAppid(WxPayConfig.APPID)#公众账号ID
        inputObj.SetMch_id(WxPayConfig.MCHID)#商户号
        inputObj.SetNonce_str(self.getNonceStr())#随机字符串

        inputObj.SetSign()#签名
        xml = inputObj.ToXml()

        startTimeStamp = self.getMillisecond()#请求开始时间
        response = self.postXmlCurl(xml, url, True, timeOut)
        result = WxPayResults.Init(response)
        self.reportCostTime(url, startTimeStamp, result)#上报请求花费时间

        return result



     #
     #  测速上报，该方法内部封装在report中，使用时请注意异常流程
     #  WxPayReport中interface_url、return_code、result_code、user_ip、execute_time_必填
     #  appid、mchid、spbill_create_ip、nonce_str不需要填入
     #  @param WxPayReport inputObj
     #  @param int timeOut
     #  @throws WxPayException
     #  @return 成功时返回，其他抛异常

    def report(self, inputObj, timeOut = 1):

        url = "https:#api.mch.weixin.qq.com/payitil/report"
        #检测必填参数
        if not inputObj.IsInterface_urlSet():
            raise WxPayException("接口URL，缺少必填参数interface_url！")
        if not inputObj.IsReturn_codeSet():
          raise WxPayException("返回状态码，缺少必填参数return_code！")
        if not inputObj.IsResult_codeSet():
           raise WxPayException("业务结果，缺少必填参数result_code！")
        if not inputObj.IsUser_ipSet():
            raise WxPayException("访问接口IP，缺少必填参数user_ip！")
        if not inputObj.IsExecute_time_Set():
            raise WxPayException("接口耗时，缺少必填参数execute_time_！")

        inputObj.SetAppid(WxPayConfig.APPID)#公众账号ID
        inputObj.SetMch_id(WxPayConfig.MCHID)#商户号
        # inputObj.SetUser_ip(_SERVER['REMOTE_ADDR'])#终端ip todo
        # inputObj.SetTime(date("YmdHis"))#商户上报时间
        inputObj.SetTime(time.strftime("YmdHis", time.localtime(time.time())))
        inputObj.SetNonce_str(self.getNonceStr())#随机字符串

        inputObj.SetSign()#签名
        xml = inputObj.ToXml()

        startTimeStamp = self.getMillisecond()#请求开始时间
        response = self.postXmlCurl(xml, url, False, timeOut)
        return response



     #
     #  生成二维码规则,模式一生成支付二维码
     #  appid、mchid、spbill_create_ip、nonce_str不需要填入
     #  @param WxPayBizPayUrl inputObj
     #  @param int timeOut
     #  @throws WxPayException
     #  @return 成功时返回，其他抛异常

    def bizpayurl(self, inputObj, timeOut = 6):

        if not inputObj.IsProduct_idSet():
            raise WxPayException("生成二维码，缺少必填参数product_id！")


        inputObj.SetAppid(WxPayConfig.APPID)#公众账号ID
        inputObj.SetMch_id(WxPayConfig.MCHID)#商户号
        inputObj.SetTime_stamp(time.time())#时间戳
        inputObj.SetNonce_str(self.getNonceStr())#随机字符串

        inputObj.SetSign()#签名

        return inputObj.GetValues()



     #
     #  转换短链接
     #  该接口主要用于扫码原生支付模式一中的二维码链接转成短链接(weixin:#wxpay/s/XXXXXX)，
     #  减小二维码数据量，提升扫描速度和精确度。
     #  appid、mchid、spbill_create_ip、nonce_str不需要填入
     #  @param WxPayShortUrl inputObj
     #  @param int timeOut
     #  @throws WxPayException
     #  @return 成功时返回，其他抛异常

     def shorturl(self, inputObj, timeOut = 6):

        url = "https:#api.mch.weixin.qq.com/tools/shorturl"
        #检测必填参数
        if not inputObj.IsLong_urlSet():
            raise WxPayException("需要转换的URL，签名用原串，传输需URL encode！")

        inputObj.SetAppid(WxPayConfig.APPID)#公众账号ID
        inputObj.SetMch_id(WxPayConfig.MCHID)#商户号
        inputObj.SetNonce_str(self.getNonceStr())#随机字符串

        inputObj.SetSign()#签名
        xml = inputObj.ToXml()

        startTimeStamp = self.getMillisecond()#请求开始时间
        response = self.postXmlCurl(xml, url, False, timeOut)
        result = WxPayResults.Init(response)
        self.reportCostTime(url, startTimeStamp, result)#上报请求花费时间

        return result



     #
     #  支付结果通用通知
     #  @param def callback
     #  直接回调函数使用方法: notify(you_def)
     #  回调类成员函数方法:notify(array(this, you_def))
     #  callback  原型为：def def_name(data)

     def notify(self, callback, msg): # todo msg

        #获取通知的数据
        xml = file_get_contents('php://input')
        #如果返回成功则验证签名
        try:
            result = WxPayResults.Init(xml)
        except  WxPayException as e:
            msg = e.errorMessage()  # todo 要直接改掉 穿进来的 msg
            return False


        return call_user_func(callback, result)



     #
     #  产生随机字符串，不长于32位
     #  @param int length
     #  @return 产生的随机字符串

     def getNonceStr(length = 32):

        chars = "abcdefghijklmnopqrstuvwxyz0123456789"
        str =""
        for i in range(length):
            str += substr(chars, mt_rand(0, strlen(chars)-1), 1)

        return str



     #  直接输出xml
     #  @param string xml

    def replyNotify(self,xml):
        return xml
        # echo xml  # todo 改为返回



     #
     #  上报数据， 上报的时候将屏蔽所有异常流程
     #  @param string usrl
     #  @param int startTimeStamp
     #  @param array data

    def reportCostTime(self, url, startTimeStamp, data):

        #如果不需要上报数据
        if WxPayConfig.REPORT_LEVENL == 0:
            return

        #如果仅失败上报
        if WxPayConfig.REPORT_LEVENL == 1 and\
             array_key_exists("return_code", data) and\
             data["return_code"] == "SUCCESS" and\
             array_key_exists("result_code", data) and\
             data["result_code"] == "SUCCESS":

            return


        #上报逻辑
        endTimeStamp = self.getMillisecond()
        objInput = new WxPayReport()
        objInput.SetInterface_url(url)
        objInput.SetExecute_time_(endTimeStamp - startTimeStamp)
        #返回状态码
        if array_key_exists("return_code", data):
            objInput.SetReturn_code(data["return_code"])

        #返回信息
        if array_key_exists("return_msg", data):
            objInput.SetReturn_msg(data["return_msg"])

        #业务结果
        if array_key_exists("result_code", data):
            objInput.SetResult_code(data["result_code"])

        #错误代码
        if array_key_exists("err_code", data):
            objInput.SetErr_code(data["err_code"])

        #错误代码描述
        if array_key_exists("err_code_des", data):
            objInput.SetErr_code_des(data["err_code_des"])

        #商户订单号
        if array_key_exists("out_trade_no", data):
            objInput.SetOut_trade_no(data["out_trade_no"])

        #设备号
        if array_key_exists("device_info", data):
            objInput.SetDevice_info(data["device_info"])


        try:
            self.report(objInput)
        except WxPayException as e:
            pass            #不做任何处理




     #  以post方式提交xml到对应的接口url
     #
     #  @param string xml  需要post的xml数据
     #  @param string url  url
     #  @param bool useCert 是否需要证书，默认不需要
     #  @param int second   url执行超时时间，默认30s
     #  @throws WxPayException

    def postXmlCurl(self, xml, url, useCert = False, second = 30):
        ch = curl_init()
        #设置超时
        curl_setopt(ch, CURLOPT_TIMEOUT, second)

        #如果有配置代理这里就设置代理
        if WxPayConfig.CURL_PROXY_HOST  != "0.0.0.0" and WxPayConfig.CURL_PROXY_PORT != 0:
            curl_setopt(ch,CURLOPT_PROXY, WxPayConfig.CURL_PROXY_HOST)
            curl_setopt(ch,CURLOPT_PROXYPORT, WxPayConfig.CURL_PROXY_PORT)

        curl_setopt(ch,CURLOPT_URL, url)
        curl_setopt(ch,CURLOPT_SSL_VERIFYPEER,TRUE)
        curl_setopt(ch,CURLOPT_SSL_VERIFYHOST,2)#严格校验
        #设置header
        curl_setopt(ch, CURLOPT_HEADER, FALSE)
        #要求结果为字符串且输出到屏幕上
        curl_setopt(ch, CURLOPT_RETURNTRANSFER, TRUE)

        if useCert is True:
            #设置证书
            #使用证书：cert 与 key 分别属于两个.pem文件
            curl_setopt(ch,CURLOPT_SSLCERTTYPE,'PEM')
            curl_setopt(ch,CURLOPT_SSLCERT, WxPayConfig.SSLCERT_PATH)
            curl_setopt(ch,CURLOPT_SSLKEYTYPE,'PEM')
            curl_setopt(ch,CURLOPT_SSLKEY, WxPayConfig.SSLKEY_PATH)

        #post提交方式
        curl_setopt(ch, CURLOPT_POST, TRUE)
        curl_setopt(ch, CURLOPT_POSTFIELDS, xml)
        #运行curl
        data = curl_exec(ch)
        #返回结果
        if data:
            curl_close(ch)
            return data
        else:
            error = curl_errno(ch)
            curl_close(ch)
            raise WxPayException("curl出错，错误码:" + error)




     #  获取毫秒级别的时间戳

    def getMillisecond(self):

        #获取毫秒的时间戳
        return int(time.time()*1000)


