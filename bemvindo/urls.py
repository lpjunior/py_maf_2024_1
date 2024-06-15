from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('saudacao/', views.saudacao, name='saudacao'),
]