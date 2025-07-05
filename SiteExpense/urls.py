from django.urls import path, include
from . import views

app_name = 'siteexpense'

urlpatterns = [
    path('', views.expense_list, name='expense_list'),
    path('submit/', views.submit_expense, name='submit_expense'),
    path('submitted/', views.expense_submitted, name='expense_submitted'),
]
