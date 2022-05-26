from django.urls import path

from . import views

urlpatterns = [
    path('webtel', views.webtel, name='webtel'),
]
