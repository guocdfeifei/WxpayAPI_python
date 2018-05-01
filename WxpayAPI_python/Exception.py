# 微信支付API异常类
class WxPayException(Exception):
    def __init__(self, *args, **kwargs):
        super().__init__(self, *args, **kwargs)
