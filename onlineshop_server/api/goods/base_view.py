import json
from django.http import HttpResponse,JsonResponse
from django.views.generic.base import View
from .models import Goods

#CBV方式编码

class GoodsListView(View):
    def get(self,request):
        """
        通过Django的View实现商品列表页
        :param request:
        :return:
        """
        goods=Goods.objects.all()[:10]
        json_data=[]
        # for good in goods:
        #     json_dict={}
        #     # 取出商品的每个字段，键值存储
        #     json_dict['name']=good.name
        #     json_dict['category']=good.category.name
        #     json_dict['market_price']=good.market_price
        #     json_data.append(json_dict)


        # from django.forms.models import model_to_dict
        # for good in goods:
        #     json_dict = model_to_dict(good)
        #     json_data.append(json_dict)
        #
        # # Object of type ImageFieldFile is not JSON serializable
        # # 返回json数据，一定要指定类型content_type='application/json'
        # return HttpResponse(json.dumps(json_data), content_type='application/json')

        from django.core import serializers
        # serialize序列化成json
        json_data=serializers.serialize('json',goods)
        json_data=json.loads(json_data)

        # In order to allow non-dict objects to be serialized set the safe parameter to False.
        #JsonResponse类中定义了json.dumps()和content_type='application/json')
        return JsonResponse(json_data,safe=False)








