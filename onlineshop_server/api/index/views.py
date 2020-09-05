from django.shortcuts import render
from django.views.generic.base import View
from django_request_mapping import request_mapping
from django.http import HttpResponse


#@request_mapping 路由映射视图
@request_mapping("/user")
class LoginView(View):

    @request_mapping('/login/',method='get')
    def login(self,request):
        return HttpResponse('ok')


# Create your views here.
