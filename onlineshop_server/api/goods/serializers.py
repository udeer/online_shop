from rest_framework import serializers
from .models import Goods, GoodsCategory, GoodsImage


class CategorySerializer3(serializers.ModelSerializer):
    """
    三级分类
    """
    class Meta:
        model=GoodsCategory
        fields='__all__'
        extra_kwargs = {
            'id': {'help_text': '商品分类id'}
        }


class CategorySerializer2(serializers.ModelSerializer):
    """
    二级分类
    """
    sub_cat = CategorySerializer3(many=True)
    class Meta:
        model=GoodsCategory
        fields='__all__'
        extra_kwargs = {
            'id': {'help_text': '商品分类id'}
        }


class CategorySerializer(serializers.ModelSerializer):
    """
    一级分类
    """
    sub_cat=CategorySerializer2(many=True)
    class Meta:
        model=GoodsCategory
        fields='__all__'
        extra_kwargs = {
            'id': {'help_text': '商品分类id'}
        }




class GoodsImageSerializer(serializers.ModelSerializer):
    class Meta:
        model=GoodsImage
        fields=('image',)


#ModelSerializer实现商品列表数据序列化
class GoodsSerializer(serializers.ModelSerializer):
    # 覆盖外键字段
    category=CategorySerializer()
    images=GoodsImageSerializer(many=True)
    class Meta:
        model=Goods
        fields='__all__'




# class GoodsSerializer(serializers.Serializer):
#     #手动添加字段
#     name=serializers.CharField(required=True,max_length=100)
#     click_num=serializers.IntegerField(default=0)
#     goods_front_image = serializers.ImageField()
#
#     def create(self, validated_data):
#         """
#         Create and return a new `Snippet` instance, given the validated data.
#         """
#         return Goods.objects.create(**validated_data)


class GoodCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model=GoodsCategory

