from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import datetime


class UserProfile(AbstractUser):
    GENDER_CHOICES = (
        ('male', '男'),
        ('female', '女')
    )
    nick_name = models.CharField(max_length=20, null=True, blank=True, verbose_name='昵称')
    birthday = models.DateField(null=True, blank=True, verbose_name='出生日期')
    gender = models.CharField(max_length=6, choices=GENDER_CHOICES, default='female', verbose_name='性别')
    mobile = models.CharField(null=True,blank=True,max_length=11, verbose_name='手机号')
    email = models.EmailField(max_length=60, null=True, blank=True, verbose_name='邮箱')

    class Meta:
        db_table='user_profile'
        verbose_name = '用户'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username

class VerifyCode(models.Model):
    code=models.CharField(max_length=10,verbose_name='验证码')
    mobile = models.CharField(max_length=11, verbose_name='手机号')
    add_time=models.DateTimeField(default=datetime.now,verbose_name='添加时间')

    class Meta:
        db_table='verify_code'
        verbose_name='短信验证码'
        verbose_name_plural=verbose_name

    def __str__(self):
        return self.code
# Create your models here.
