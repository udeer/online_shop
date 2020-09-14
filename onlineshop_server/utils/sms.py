from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.request import CommonRequest

ACCESS_KEY_ID = "你的id"  #用户AccessKey
ACCESS_KEY_SECRET = "你的密码"  #Access Key Secret

class AliyunSms:
    """
    阿里云短信服务SDK
    """
    def __init__(self,signName,templateCode):
        self.signName = signName
        self.templateCode = templateCode
        self.client = client = AcsClient(ACCESS_KEY_ID,ACCESS_KEY_SECRET,'cn-hangzhou')

    def send_sms(self, mobile, code):
        request = CommonRequest()
        request.set_accept_format('json')
        request.set_domain('dysmsapi.aliyuncs.com')
        request.set_method('POST')
        request.set_protocol_type('https')  # https | http
        request.set_version('2017-05-25')
        request.set_action_name('SendSms')

        request.add_query_param('RegionId', "cn-hangzhou")
        request.add_query_param('PhoneNumbers', mobile)
        request.add_query_param('SignName', self.signName)
        request.add_query_param('TemplateCode', self.templateCode)
        request.add_query_param('TemplateParam', {"code": code})
        response = self.client.do_action_with_exception(request)
        response=eval(response.decode())#bytes转str类型
        return response



# if __name__=="__main__":
#     # 短语发送对象
#     sms = AliyunSms("海购生鲜", "SMS_199200099")
#     sms.send_sms(mobile=18367131471, code={"code": 1111})
