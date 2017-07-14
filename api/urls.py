from django.conf.urls import url, include
from rest_framework import routers
from api import views

# router = routers.DefaultRouter()
# router.register(r'conta', views.ContaViewSet, 'conta-list')

urlpatterns = [
    
    #CONTA
    url(r'^conta/(?P<pk>[0-9]+)/extrato/$',
        views.ContaViewSet.as_view({'get':'extrato'})),
    url(r'^conta/(?P<pk>[0-9]+)/transferencia/$',
        views.ContaViewSet.as_view({'post':'transferencia'})),
    url(r'^conta/(?P<pk>[0-9]+)/saque/$',
        views.ContaViewSet.as_view({'post':'saque'})),
    url(r'^conta/(?P<pk>[0-9]+)/$',
        views.ContaViewSet.as_view({'get':'retrieve', 'post':'update'})),
    url(r'^conta/$',
        views.ContaViewSet.as_view({'get':'list', 'post':'create'})),
    
    #CAIXA
    url(r'^caixa/', views.CaixaView.as_view()),
]