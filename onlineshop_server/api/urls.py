from rest_framework.routers import DefaultRouter

from api.goods.views import GoodsListViewSet, CategoryViewSet
from api.trade.views import ShoppingCartViewSet, OrderVewSet
from api.user_operation.views import UserFavViewSet, UserCommentsViewSet, AddressViewSet
from api.users.views import VerifyCodeViewSet, UserViewSet
from django.urls import path, include
from django_request_mapping import UrlPattern

router=DefaultRouter()
#商品
router.register(r'goods', GoodsListViewSet,basename='goods')
#商品分类
router.register(r'categorys', CategoryViewSet,basename='categorys')
#用户收藏
router.register(r'userfavs', UserFavViewSet,basename='userfavs')
#用户留言
router.register(r'comments', UserCommentsViewSet,basename='comments')
#用户地址
router.register(r'address', AddressViewSet,basename='address')
#短信验证码
router.register(r'code', VerifyCodeViewSet,basename='code')
#用户
router.register(r'users', UserViewSet,basename='users')
#购物车
router.register(r'shopcarts', ShoppingCartViewSet,basename='shopcarts')
#订单
router.register(r'orders', OrderVewSet,basename='orders')

urlpatterns = [
    path('', include(router.urls)),
]


