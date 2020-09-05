import time

from django.shortcuts import render
from rest_framework import viewsets
from rest_framework import mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.authentication import SessionAuthentication
from api.trade.serializers import ShopCartSerializer, ShopCartDetailSerializer, OrderSerializer, OrderDetailSerializer
from api.trade.models import ShoppingCart, OrderGoods,OrderInfo
from utils.permissions import IsOwnerOrReadOnly





class ShoppingCartViewSet(viewsets.ModelViewSet):
    """
    list:
    获取购物车列表
    create:
    添加商品加入购物车
    update:
    更新购物车商品数量
    retrieve:
    查询指定的购物车商品详情
    delete:
    从购物车中删除商品
    """
    serializer_class = ShopCartSerializer
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)  # API操作:支持登录者认证和所有者权限认证
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)  # API访问:支持JWT认证
    lookup_field = 'goods_id' #id是服务器生成的前端不知道，通过goods_id查询增删改查操作

    def get_serializer_class(self):
        if self.action=='list':
            return ShopCartDetailSerializer
        else:
            return ShopCartSerializer


    def get_queryset(self):
        return ShoppingCart.objects.filter(user=self.request.user) #过滤当前用户的购物车记录 get_queryset在mixin都要用到


class OrderVewSet(mixins.ListModelMixin,mixins.CreateModelMixin,mixins.RetrieveModelMixin,mixins.DestroyModelMixin,viewsets.GenericViewSet):
    """
    list:
    获取所有订单
    create:
    创建订单
    delete:
    删除订单
    """
    serializer_class = OrderSerializer
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)  # API操作:支持登录者认证和所有者权限认证
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)  # API访问:支持JWT认证

    def get_serializer_class(self):
        if self.action == "retrieve":
            return OrderDetailSerializer
        else:
            return OrderSerializer
    # 1.将购物车中的商品保存到OrderGoods中
    # 2.清空购物车
    def perform_create(self, serializer):
        order=serializer.save()
        # 获取购物车所有商品
        shop_carts=ShoppingCart.objects.filter(user=self.request.user)
        for shop_cart in shop_carts:
            order_goods=OrderGoods()
            order_goods.goods=shop_cart.goods
            order_goods.goods_num=shop_cart.nums
            order_goods.order=order
            order_goods.save()
            # 清空购物车
            shop_cart.delete()

        return order



    def get_queryset(self):
        return OrderInfo.objects.filter(user=self.request.user)
# Create your views here.