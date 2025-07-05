from django.urls import path
from . import views
from . import views_ledger
from . import views_reports

app_name = 'accounting'

urlpatterns = [
    path('', views.index, name='index'),
    path('journals/', views.journal_list, name='journal_list'),
    path('journals/new/', views.journal_create, name='journal_create'),
    path('journals/<int:pk>/post/', views.journal_post, name='journal_post'),
    path('capital-contributions/', views.capital_contribution_list, name='capital_contribution_list'),
    path('capital-contributions/new/', views.capital_contribution_create, name='capital_contribution_create'),
    path('balance-sheet/', views.balance_sheet, name='balance_sheet'),
    path('accounts/<int:pk>/ledger/', views_ledger.account_ledger, name='account_ledger'),
    path('accounts/', views_ledger.account_list, name='account_list'),
    path('reports/trial-balance/', views_reports.trial_balance, name='trial_balance'),
    path('reports/income-statement/', views_reports.income_statement, name='income_statement'),
    path('reports/general-ledger/', views_reports.general_ledger_report, name='general_ledger'),
    path('reports/cash-flow/', views_reports.cash_flow_statement, name='cash_flow'),
    path('reports/journal/', views_reports.journal_report, name='journal_report'),
    path('accounts/new/', views_ledger.account_create, name='account_create'),
    path('accounts/<int:pk>/edit/', views_ledger.account_edit, name='account_edit'),
]
