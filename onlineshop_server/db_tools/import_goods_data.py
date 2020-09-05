#独立使用django中的model
import os,sys

#  获取当前文件的路径，以及路径的父级文件夹名
pwd=os.path.dirname(os.path.realpath(__file__))
# 将项目目录加入setting
sys.path.append(pwd+"../")
# manage.py中
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'onlineshop_server.settings')

import  django
django.setup()

# 这行代码必须在初始化django之后
from api.goods.models import Goods, GoodsImage, GoodsCategory

from db_tools.data.product_data import row_data

for goods_detail in row_data:
    goods=Goods()
    goods.name=goods_detail['name']
    goods.market_price=float(int(goods_detail['market_price'].replace('￥','').replace('元','')))
    goods.shop_price = float(int(goods_detail['sale_price'].replace('￥', '').replace('元', '')))
    goods.goods_brief = goods_detail["desc"] if goods_detail["desc"] is not None else ""
    goods.goods_desc = goods_detail["goods_desc"] if goods_detail["goods_desc"] is not None else ""
    category_name = goods_detail["categorys"][-1]
    category = GoodsCategory.objects.filter(name=category_name)
    if category:
        goods.category = category[0]
    goods.save()
    for goods_image in goods_detail["images"]:
        goods_image_instance = GoodsImage()
        goods_image_instance.image = goods_image
        goods_image_instance.goods = goods
        goods_image_instance.save()



