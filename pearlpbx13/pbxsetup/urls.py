from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('pjsip.conf', views.pjsip_conf, name='pjsip.conf'),
    path('extensions.ael', views.extensions_ael, name='extensions.ael')
]
