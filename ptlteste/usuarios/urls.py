from django.urls import path, include
from rest_framework import routers
from .views import gerar_token, UsuarioViewSet,do_login, do_logout, index, editar,CadastrarUserView, cadastrar, search_by_cep
from django.conf.urls import url, include
from rest_framework import permissions, authentication
from rest_framework_jwt.views import obtain_jwt_token

app_name = 'usuarios'


router = routers.DefaultRouter()
router.register(r'usuarios', UsuarioViewSet)

urlpatterns = [

    path('index/', index , name="index"),
    path('', index , name="index"),
    path('editar/<pk>', editar , name="editar"),
    path('cadastrar/',cadastrar  , name="cadastrar"), #templeate
    path('api_cadastrar/', CadastrarUserView.as_view() , name="api_cadastrar"), #endpoint

    path('api/', include(router.urls)),
    path('gerar_token/', gerar_token, name = "gerar_token"),
    path('accounts/login/', do_login, name = "login"),
    path('logout/', do_logout, name = "logout"),
    path('accounts/', include('django.contrib.auth.urls')),

    # cep
    path('dadoscep/', search_by_cep, name = "dadoscep"),

]
