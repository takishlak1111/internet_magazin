from django.urls import path
from . import views

app_name = 'catalog'

urlpatterns = [

    path('', views.product_list, name='product_list'),

    path('category/<slug:slug>/', views.category_detail, name='category_detail'),

    path('brand/<slug:slug>/', views.brand_detail, name='brand_detail'),

    path('product/<slug:slug>/', views.product_detail, name='product_detail'),

    path('search/', views.product_search, name='product_search'),
]