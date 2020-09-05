from django.contrib import admin
from .models import ShoppingCart, OrderInfo, OrderGoods


class ShoppingCartAdmin(admin.ModelAdmin):
    list_display = ["user", "goods", "nums"]


class OrderInfoAdmin(admin.ModelAdmin):
    list_display = ["user", "order_sn",  "trade_no", "pay_status", "post_script", "order_mount",
                    "order_mount", "pay_time", "add_time"]



admin.site.register(ShoppingCart, ShoppingCartAdmin)
admin.site.register(OrderInfo, OrderInfoAdmin)