from django.shortcuts import render
from rest_framework import mixins
from rest_framework import viewsets
from api.user_operation.models import UserFav, UserComments, UserAddress
from api.user_operation.serializers import UserFavSerializer,UserFavlistSerializer,UserCommentsSerializer,UserAddressSerializer
from rest_framework.permissions import IsAuthenticated
from utils.permissions import IsOwnerOrReadOnly
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.authentication import SessionAuthentication


class UserFavViewSet(mixins.CreateModelMixin,mixins.DestroyModelMixin,mixins.RetrieveModelMixin,mixins.ListModelMixin,viewsets.GenericViewSet):
    """
    list:
    获取用户收藏记录
    create:
    添加收藏
    delete:
    删除收藏
    retrieve:
    查询某条收藏
    """
    #queryset =UserFav.objects.all()
    serializer_class =UserFavSerializer
    permission_classes = (IsAuthenticated,IsOwnerOrReadOnly)#API操作:支持登录者认证和所有者权限认证
    authentication_classes =(JSONWebTokenAuthentication,SessionAuthentication) #API访问:支持JWT认证和Session认证
    lookup_field ='goods_id'#前端通过商品id查询收藏记录和提交收藏

    def get_queryset(self):
        # 过滤当前用户的收藏记录列表
        return UserFav.objects.filter(user=self.request.user)

    # 动态配置序列化类
    #1.serializer_class =UserFavSerializer(用户收藏)只需要返回商品id,而用户收藏商品详情需要其他序列化类
    # 2.根据不同的传入请求提供不同的序列化，需要动态配置serializer
    def get_serializer_class(self):
        if self.action=='list':
            return UserFavlistSerializer
        elif self.action=='create':
            return UserFavSerializer
        return UserFavSerializer


class UserCommentsViewSet(mixins.ListModelMixin,mixins.CreateModelMixin,mixins.DestroyModelMixin,viewsets.GenericViewSet):
    """
    list:
    获取用户留言列表
    create:
    添加留言
    delete:
    删除留言
    """
    serializer_class = UserCommentsSerializer
    permission_classes = (IsAuthenticated,IsOwnerOrReadOnly)#API操作:支持登录者认证和所有者权限认证
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)  # API访问:支持JWT认证和Session认证

    def get_queryset(self):
        # 过滤当前用户的留言记录列表
        return UserComments.objects.filter(user=self.request.user)


class AddressViewSet(viewsets.ModelViewSet):
    serializer_class = UserAddressSerializer
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)  # API操作:支持登录者认证和所有者权限认证
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)  # API访问:支持JWT认证和Session认证

    def get_queryset(self):
        # 过滤当前用户的留言记录列表
        return UserAddress.objects.filter(user=self.request.user)



# Create your views here.