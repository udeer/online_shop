from django_request_mapping import UrlPattern
from api.index.views import LoginView

urlpatterns = UrlPattern()

#注册路由
urlpatterns.register(LoginView)
