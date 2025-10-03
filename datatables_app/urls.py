from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('customers/', views.customer_list, name='customer_list'),
    path('products/', views.product_list, name='product_list'),
    path('api/customers/', views.get_customers_json, name='get_customers_json'),
    path('api/products/', views.get_products_json, name='get_products_json'),
 
   
]