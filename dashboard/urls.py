from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.dashboard_home, name='dashboard_home'),
    path('login/', views.owner_login, name='owner_login'),
    path('logout/', views.owner_logout, name='owner_logout'),
    path('products/', views.product_list, name='product_list'),
    path('products/add/', views.product_add, name='product_add'),
    path('products/edit/<int:pk>/', views.product_edit, name='product_edit'),
    path('products/<int:product_pk>/delete-image/<int:image_pk>/', views.product_image_delete, name='product_image_delete'),
    path('products/delete/<int:pk>/', views.product_delete, name='product_delete'),
    path('orders/', views.order_list, name='order_list'),
    path('orders/status/<int:pk>/', views.order_status_update, name='order_status_update'),
    path('analytics/', views.analytics_view, name='analytics_view'),
]
