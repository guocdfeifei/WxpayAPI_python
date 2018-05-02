# 微信支付API异常类
class WxPayException(Exception):
    def __init__(self, *args, **kwargs):
        super(self, WxPayException).__init__(self, *args, **kwargs)
