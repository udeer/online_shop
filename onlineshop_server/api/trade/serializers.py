import time

from rest_framework import serializers
from api.trade.models import ShoppingCart,OrderInfo,OrderGoods
from api.goods.models import Goods
from api.goods.serializers import GoodsSerializer

class OrderGoodsSerializer(serializers.ModelSerializer):
    """订单商品序列化器类"""
    goods=GoodsSerializer(many=False) #重载goods字段,嵌套序列化获取商品详情
    class Meta:
        model=OrderGoods
        fields="__all__"


class OrderDetailSerializer(serializers.ModelSerializer):
    """订单详情序列化器类"""
    order_goods=OrderGoodsSerializer(many=True)#related_name一对多关系
    class Meta:
        model=OrderInfo
        fields="__all__"


class OrderSerializer(serializers.ModelSerializer):
    # 隐藏自定义user字段 获取当前登录的用户
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    pay_status = serializers.CharField(read_only=True)#不允许写，只做序列化显示
    order_sn=serializers.CharField(read_only=True)
    trade_no = serializers.CharField(read_only=True)
    pay_time = serializers.CharField(read_only=True)


    def generate_order_sn(self):
        #生成订单号
        from random import Random
        random_ins =Random()
        order_sn='{time}{userid}{random_str}'.format(time=time.strftime('%Y%m%d%H%M%S'),userid=self.context["request"].user.id,random_str=random_ins.randint(10, 99))
        return order_sn

    def validate(self, attrs):
        #validate中添加order_sn
        attrs['order_sn']=self.generate_order_sn()
        return attrs

    class Meta:
        model=OrderInfo
        fields="__all__"



class ShopCartSerializer(serializers.Serializer):
    # 隐藏自定义user字段 获取当前登录的用户
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    nums=serializers.IntegerField(required=True,min_value=1,error_messages={
        'min_value':'商品数量不能小于1',
        'required':'请选择商品购买数量'
    },label='商品数量')
    # 继承Serializer 必须指定queryset对象，ModelSerializer和model已关联不需要指定
    # goods是一个外键，可以通过这方法获取goods object中所有的值
    goods=serializers.PrimaryKeyRelatedField(required=True,queryset=Goods.objects.all(),label='商品')


    def create(self, validated_data):
        #定义create方法 创建购物车
        #validated_data是全部字段验证通过的数据
        # 获取当前用户
        # view中:user=self.request.user；serizlizer中:user=self.context["request"].user
        user=self.context['request'].user
        goods_nums=validated_data['nums']
        goods=validated_data['goods']#Goods的对象

        # 查询记录是否存在，存在则进行数量加，不存在则新创建
        shopcart=ShoppingCart.objects.filter(user=user,goods=goods)
        if shopcart:
            shopcart=shopcart[0]
            shopcart.nums+=goods_nums
            shopcart.save()
        else:
            #添加商品到购物车
            shopcart=ShoppingCart.objects.create(**validated_data)
        #得到购物车做反序列化
        return shopcart


    def update(self, instance, validated_data):
        #定义update方法 修改购物车商品数量
        instance.nums=validated_data['nums']
        instance.save()
        return instance


class ShopCartDetailSerializer(serializers.ModelSerializer):
    #自定义goods字段嵌套序列化类 得到goods详情
    goods=GoodsSerializer(many=False)
    class Meta:
        model=ShoppingCart
        fields=('goods','nums')


