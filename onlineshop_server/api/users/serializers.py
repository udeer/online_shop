from datetime import datetime, timedelta
import re

from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from api.users.models import VerifyCode

User=get_user_model()

class VerifyCodeSerializer(serializers.Serializer):
    """短信验证码序列化类"""
    """"
       不用ModelSerializer原因：发送验证码只需要提交手机号码
    """
    mobile=serializers.CharField(max_length=11,help_text="手机号")

    def validate_mobile(self, mobile):
        """
        验证手机号
        :param data:
        :return:
        """
        #手机是否注册
        if User.objects.filter(mobile=mobile).count():
            raise serializers.ValidationError("手机号码已经存在")

        #验证手机号是否合法
        regexp = "^[1][3,4,5,7,8][0-9]{9}$"
        if not re.match(regexp,mobile):
            raise serializers.ValidationError("手机号码格式不正确")

        #验证发送频率
        one_mintue_ago=datetime.now()-timedelta(hours=0, minutes=1, seconds=0)#获取一分钟以前的时间
        if VerifyCode.objects.filter(add_time__gt=one_mintue_ago,mobile=mobile):
            # 如果添加时间大于一分钟以前的时间，则在这一分钟内已经发过短信，不允许再次发送
            raise serializers.ValidationError('距离上次发送未超过60s')
        return mobile


class UserRegSerializer(serializers.ModelSerializer):
    """用户信息详情序列化类"""
    #code字段新声明
    code = serializers.CharField(write_only=True,required=True,min_length=4,max_length=4,help_text='短信验证码',label='验证码',error_messages={'blank': '请输入验证码','required':'该字段是必填项','max_length':'验证码长度是4位','min_length':'验证码长度是4位',})
    # 自定义验证字段
    username=serializers.CharField(required=True,allow_blank=False,label='用户名',help_text='用户名',validators=[UniqueValidator(queryset=User.objects.all(), message='用户已存在')])

    password = serializers.CharField(write_only=True,required=True,label='密码',help_text='密码',style={'input_type': 'password'})

    def validate_code(self, code):
        #validate_empty_values函数用于验证单个字段
        verify_codes=VerifyCode.objects.filter(mobile=self.initial_data['username']).order_by('-add_time') # self.initial_data 为用户前端传过来的所有值
        if verify_codes:
            last_record=verify_codes[0]
            five_mintue_ago = datetime.now() - timedelta(hours=0, minutes=5, seconds=0)  # 获取五分钟前的时间
            if five_mintue_ago > last_record.add_time:
                raise serializers.ValidationError('验证码过期',code=code)
            elif last_record.code!=code:
                raise serializers.ValidationError('验证码错误')
            # return code #code只用于验证，不需要保存到数据库中
        else:
            #没有查到该手机号对应的验证码
            raise serializers.ValidationError('手机号验证码不存在')

    def validate(self, attrs):
        #validate函数用于验证所有字段
        attrs['mobile']=attrs['username']
        del attrs['code'] #删除User表不存在的code字段
        return attrs #attrs将作为参数传递到.create()

    class Meta:
        #生成ModelSerializer字段
        model=User
        fields=("username","code","mobile","password",)#username是Django自带必填字段，与mobile保持一致


class  UserDetailSerializer(serializers.ModelSerializer):
    """用户信息详情序列化类"""

    class Meta:
        model = User
        fields = ("nick_name", "gender", "birthday", "email",'mobile')


