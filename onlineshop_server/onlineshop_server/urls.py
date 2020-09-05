"""onlineshop_server URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.conf.urls import url
from django.contrib import admin
from django.views.static import serve
from django.urls import path,include
from rest_framework.documentation import include_docs_urls
from rest_framework_jwt.views import obtain_jwt_token
from onlineshop_server.settings import MEDIA_ROOT
from rest_framework.authtoken import views

# #调用viewsets的子类.as_view方法
# goods_list = GoodsListViewSet.as_view({
#     'get': 'list',
#
# })
#

urlpatterns = [
    #基于Django的商品列表页
    # url(r'goods/$',GoodsListView.as_view(),name='goods-list'),
    # url(r'goods/$',goods_list,name='goods')
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
    url(r'^media/(?P<path>.*)$',serve,{'document_root':MEDIA_ROOT}),
    url(r'^api-auth/', include('rest_framework.urls')),#DRF登录
    url(r'^docs/',include_docs_urls(title='API 文档')),#DRF文档
    #DRF认证接口
    path('api-token-auth/', views.obtain_auth_token),
    #JWT认证接口
    path('login/', obtain_jwt_token),

]

# urlpatterns += router.urls#配置API根路由