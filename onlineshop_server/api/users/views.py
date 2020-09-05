from django.contrib.auth import get_user_model
from django.http import HttpResponse
from django.shortcuts import render
from random import choice
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from django.views.generic.base import View
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework import mixins
from utils.sms import AliyunSms
from .serializers import VerifyCodeSerializer, UserRegSerializer, UserDetailSerializer
from api.users.models import VerifyCode
from rest_framework import status, permissions
from rest_framework_jwt.serializers import jwt_encode_handler,jwt_payload_handler
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.authentication import SessionAuthentication
User=get_user_model()

class CustomBackend(ModelBackend):
    """自定义用户登录验证"""
    def authenticate(self,request,username=None, password=None, **kwargs):
        try:
            user = User.objects.get(Q(username=username) | Q(mobile=username))
            if user.check_password(password):
                return user
        except Exception as e:
            return None


class VerifyCodeViewSet(mixins.CreateModelMixin,viewsets.GenericViewSet):
    """
    create:
    发送短信验证码
    """
    serializer_class = VerifyCodeSerializer

    def generate_code(self):
        """生成验证码"""
        seeds='1234567890'
        random_str=[]
        for i in range(4):
            random_str.append(choice(seeds))
        return ''.join(random_str)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # raise_exception=True表示is_valid验证失败，就直接抛出异常，被DRF捕捉到，直接会返回400错误，不会往下执行
        mobile=serializer.validated_data['mobile']
        code = self.generate_code()
        #发送验证码
        sms=AliyunSms("海购生鲜", "SMS_199200099")
        sms_status=sms.send_sms(mobile=mobile,code=code)
        if sms_status['Code']!="OK":
            return Response({
                'mobile':sms_status['Message']
            },status.HTTP_400_BAD_REQUEST)
        else:
            # 在短信发送成功之后保存验证码
            code_record = VerifyCode(mobile=mobile, code=code)
            code_record.save()
            return Response({
                'mobile': mobile
            },status=status.HTTP_201_CREATED)


class UserViewSet(mixins.CreateModelMixin,mixins.RetrieveModelMixin,mixins.UpdateModelMixin,viewsets.GenericViewSet):
    """
    create:
    向服务器提交创建一个新用户
    retrieve:
    获取当前用户个人信息
    update:
    更新当前用户个人信息
    partial_update:
    部分更新当前用户个人信息
    """
    queryset = User.objects.all()
    serializer_class = UserRegSerializer
    authentication_classes = (JSONWebTokenAuthentication,SessionAuthentication)

    # 动态权限配置
    #1.用户访问create不应该有权限限制
    #2.用户获取或更新个人信息必须登录
    def get_permissions(self):
        if self.action == 'retrieve':
            return [permissions.IsAuthenticated()]
        elif self.action == 'create':
            return []
        return []

    # 动态配置序列化类
    #1.serializer_class = UserRegSerializer(用户注册)只会返回username和mobile，个人信息资料需要有更多字段UserDetailSerializer
    #2.根据不同的传入请求提供不同的序列化，需要动态配置serializer
    def get_serializer_class(self):
        if self.action == 'retrieve':
            return UserDetailSerializer
        elif self.action == 'create':
            return UserRegSerializer
        return UserDetailSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        #添加逻辑，生成user的token并返回
        user=self.perform_create(serializer)
        re_dict=serializer.data
        payload=jwt_payload_handler(user)
        re_dict['token']=jwt_encode_handler(payload)
        re_dict['name']=user.username
        headers = self.get_success_headers(serializer.data)
        return Response(re_dict, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        #保存函数
        return serializer.save() #.save()调用.create()返回user

    def get_object(self):
        # RetrieveModelMixin可以获取用户详情，但是并不知道用户的id。重写get_object()方法返回值return obj
        # 获当前登录用户对象
        return self.request.user


# Create your views here.


