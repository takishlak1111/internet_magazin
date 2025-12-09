from django.urls import path
from . import views

app_name = 'cart'

urlpatterns = [
    path('', views.view, name='view'),
    path('add/<int:product_id>/', views.add, name='add'),
    path('remove/<int:item_id>/', views.remove, name='remove'),
]