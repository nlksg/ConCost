from django.urls import path
from . import views

app_name = 'purchase'

urlpatterns = [
    path('', views.purchase_list, name='purchase_list'),
    path('new/', views.purchase_create, name='purchase_create'),
    path('<int:pk>/edit/', views.purchase_edit, name='purchase_edit'),
    path('<int:pk>/approve/', views.approve_purchase, name='approve_purchase'),

    # Item (Catalog) URLs
    path('items/', views.item_list, name='item_list'),
    path('items/new/', views.item_create, name='item_create'),
    path('items/<int:pk>/edit/', views.item_edit, name='item_edit'),
    path('items/<int:pk>/delete/', views.item_delete, name='item_delete'),
]
