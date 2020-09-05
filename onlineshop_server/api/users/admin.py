from django.contrib import admin
# import xadmin
# from xadmin import views
from .models import VerifyCode,UserProfile


# class BaseSetting(object):
#     enable_themes = True
#     use_bootswatch = True
#
#
# class GlobalSettings(object):
#     site_title = "慕学生鲜后台"
#     site_footer = "mxshop"
#     # menu_style = "accordion"


class VerifyCodeAdmin(admin.ModelAdmin):
    list_display = ['code', 'mobile', "add_time"]

class UserProfileAdmin(admin.ModelAdmin):
    pass

admin.site.register(VerifyCode, VerifyCodeAdmin)
admin.site.register(UserProfile, UserProfileAdmin)
# xadmin.site.register(views.BaseAdminView, BaseSetting)
# xadmin.site.register(views.CommAdminView, GlobalSettings)
# Register your models here.
