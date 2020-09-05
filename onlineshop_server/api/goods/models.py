from datetime import datetime

from django.db import models
from extra_apps.DjangoUeditor.models import UEditorField

class GoodsCategory(models.Model):
    CATEGORY_TYPE=(
        (1, '一级目录'),
        (2, '二级目录'),
        (3, '三级目录'),
    )

    name=models.CharField(max_length=30,default='',verbose_name='类别名',help_text='类别名')
    code=models.CharField(max_length=30,default='',verbose_name='类别code',help_text='类别code')
    desc=models.TextField(default='',verbose_name='类别描述',help_text='类别描述')
    category_type=models.IntegerField(choices=CATEGORY_TYPE,verbose_name='类目级别',help_text='类目级别')
    parent_category=models.ForeignKey('self',on_delete=models.CASCADE,null=True,blank=True,verbose_name='父类目级别',help_text='父目录',related_name='sub_cat')
    is_tab = models.BooleanField(default=False,verbose_name='是否导航',help_text='是否导航' )
    add_time=models.DateTimeField(default=datetime.now,verbose_name='添加时间')

    class Meta:
        db_table="goods_category"
        verbose_name='商品类别'
        verbose_name_plural=verbose_name
        ordering = ['id']

    def __str__(self):
        return self.name


class GoodsCategoryBrand(models.Model):
    """
    品牌名
    """
    category=models.ForeignKey(GoodsCategory,on_delete=models.CASCADE,null=True,blank=True,verbose_name='商品类目')
    name=models.CharField(max_length=20,default='',verbose_name='品牌名',help_text='品牌名')
    desc=models.TextField(max_length=300,default='',verbose_name='品牌描述',help_text='品牌描述')
    image=models.ImageField(max_length=200,upload_to='brands/images',verbose_name='图片')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')

    class Meta:
        db_table="goods_category_brand"
        verbose_name = '品牌'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Goods(models.Model):
    """
    商品
    """
    category=models.ForeignKey(GoodsCategory,on_delete=models.CASCADE,verbose_name='所属商品类目')
    goods_sn=models.CharField(max_length=50,default='',verbose_name='商品唯一货号')
    name=models.CharField(max_length=50,default='',verbose_name='商品名')
    click_num=models.IntegerField(default=0,verbose_name='点击数')
    sold_num=models.IntegerField(default=0,verbose_name='销售量')
    fav_num=models.IntegerField(default=0, verbose_name="收藏数")
    goods_num=models.IntegerField(default=0, verbose_name="库存数")
    market_price=models.FloatField(default=0, verbose_name="市场价格")
    shop_price=models.FloatField(default=0, verbose_name="本店价格")
    goods_brief=models.TextField(max_length=300,verbose_name='商品简短描述')
    goods_desc=UEditorField(default='',width=1000,height=300,imagePath="goods/images/",filePath="goods/files/",verbose_name=u'内容')
    ship_free=models.BooleanField(default=True, verbose_name="是否承担运费")
    goods_front_image = models.ImageField(max_length=200,upload_to="goods/images/", null=True, blank=True, verbose_name="封面图")
    is_new=models.BooleanField(default=False, verbose_name="是否新品")
    is_hot=models.BooleanField(default=False, verbose_name="是否热销")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        db_table = "goods"
        verbose_name = '商品'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name





class GoodsImage(models.Model):
    goods=models.ForeignKey(Goods,on_delete=models.CASCADE,related_name='images',verbose_name='商品')
    image=models.ImageField(max_length=200,upload_to="", null=True, blank=True,verbose_name="图片")
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')

    class Meta:
        db_table = "goods_image"
        verbose_name='商品轮播图'
        verbose_name_plural=verbose_name

    def __str__(self):
        return self.goods.name


class Banner(models.Model):
    goods = models.ForeignKey(Goods,on_delete=models.CASCADE, verbose_name='商品名')
    image = models.ImageField(upload_to='banner/images', verbose_name='轮播图')
    index = models.IntegerField(default=0, verbose_name="轮播顺序")
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')

    class Meta:
        db_table="banner"
        verbose_name = '轮播商品'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.goods.name

# Create your models here.
