from django.urls import path
from . import views

urlpatterns = [
    path('get-warehous', views.get_warehous, name='get-warehous'),
    path('get-materials', views.get_materials, name='get-materials'),
    path('get-products', views.get_products, name='get-products'),
    path('calculate', views.calculate, name='calculate'),
]
