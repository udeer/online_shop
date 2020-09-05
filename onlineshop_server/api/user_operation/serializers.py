from rest_framework import serializers
from.models import UserFav,UserComments,UserAddress
from rest_framework.validators import UniqueTogetherValidator
from api.goods.serializers import GoodsSerializer

class UserFavSerializer(serializers.ModelSerializer):
    # 隐藏自定义user字段 获取当前登录的用户
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    class Meta:
        model=UserFav
        fields=("user","goods",'id')#取消收藏必须用到id
        #Validator实现联合唯一性，一个商品只能收藏一次
        validators = [
            UniqueTogetherValidator(
                queryset=UserFav.objects.all(),
                fields=['user', 'goods'],
                message='已经收藏'
            )
        ]


class UserFavlistSerializer(serializers.ModelSerializer):
    """用户收藏列表序列化类"""
    goods=GoodsSerializer()  #自定义goods字段 通过goods_id外键关系获取收藏的商品详情，需要嵌套商品的序列化
    class Meta:
        model = UserFav
        fields = ("goods", "id")


class UserCommentsSerializer(serializers.ModelSerializer):
    """用户留言序列化类"""

    # 获取当前登录的用户
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    add_time=serializers.DateTimeField(read_only=True,format='%Y-%m-%d %H:%M')#自定义add_time字段 read_only只返回序列化,不用提交
    class Meta:
        model = UserComments
        fields = ("user", "message_type","subject","message","file","id","add_time")


class UserAddressSerializer(serializers.ModelSerializer):
    """收货地址序列化类"""

    # 获取当前登录的用户
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    add_time = serializers.DateTimeField(read_only=True, format='%Y-%m-%d %H:%M')  # 自定义add_time字段 read_only只返回序列化,不用提交
    class Meta:
        model = UserAddress
        fields = ("user", "province","city","district","address","signer_name","signer_mobile",'add_time','id')
