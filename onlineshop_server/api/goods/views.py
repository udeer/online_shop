from django.shortcuts import render
from rest_framework.pagination import PageNumberPagination

from rest_framework.views import APIView
from rest_framework.response import Response

from .filters import GoodsFilter
from .models import Goods,GoodsCategory
from .serializers import GoodsSerializer, CategorySerializer
from rest_framework import mixins
from rest_framework import generics
from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.authentication import TokenAuthentication



class GoodsPagination(PageNumberPagination):
    """
    自定义分页功能
    """
    # 默认每页显示的个数
    page_size = 10
    # 前端动态改变每页显示的个数
    page_size_query_param = 'page_size'
    # 页码参数
    page_query_param = 'page'
    # 最多能显示多少页
    max_page_size = 100

# class GoodsListView(generics.ListAPIView):
#     """
#     商品列表API
#     """
#     queryset = Goods.objects.all()
#     serializer_class = GoodsSerializer
#     pagination_class = GoodsPagination

# class GoodsListView(mixins.ListModelMixin,generics.GenericAPIView):
#     """
#     商品列表API
#     """
#     #GenericAPIView的使用必须配置queryset和serializer_class
#     queryset = Goods.objects.all()[:10]
#     serializer_class = GoodsSerializer
#
#     #重载get方法，调用ListModelMixin下的list方法做序列化、分页逻辑
#     def get(self,request,*args,**kwargs):
#         return self.list(request,*args,**kwargs)
class GoodsListViewSet(mixins.ListModelMixin,mixins.RetrieveModelMixin,viewsets.GenericViewSet):
    """
    list:
    获取所有商品数据
    retrieve:
    获取指定商品的详情数据
    """

    queryset = Goods.objects.all().order_by('id')
    serializer_class = GoodsSerializer
    pagination_class = GoodsPagination
    filter_backends = [DjangoFilterBackend,filters.SearchFilter,filters.OrderingFilter]
    #设置filter的类为我们自定义的类
    filter_class = GoodsFilter
    # 搜索,=name表示精确搜索，也可以使用各种正则表达式
    search_fields = ('=name', '=goods_brief')
    # 排序
    ordering_fields = ('sold_num', 'add_time')



    # def get_queryset(self):
    #     queryset=Goods.objects.all()
    #     price_min=self.request.query_params.get('price_min',0)
    #     if price_min:
    #         queryset=queryset.filter(shop_price__gt=int(price_min))
    #     return queryset


class CategoryViewSet(mixins.ListModelMixin,mixins.RetrieveModelMixin,viewsets.GenericViewSet):
    """
    list:
    获取所有商品分类数据
    retrieve:
    获取指定商品分类详情数据
    """
    queryset = GoodsCategory.objects.all()
    serializer_class =CategorySerializer


# Create your views here.
