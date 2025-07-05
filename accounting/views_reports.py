from django.shortcuts import render
from .models import Account, Journal, JournalEntry
from django.db.models import Sum, Q
from django.utils import timezone
from datetime import date

def trial_balance(request):
    accounts = Account.objects.filter(active=True).order_by('account_code')
    rows = []
    total_debit = 0
    total_credit = 0
    for account in accounts:
        debit = JournalEntry.objects.filter(account=account, journal__posted=True, journal__approved=True).aggregate(Sum('debit'))['debit__sum'] or 0
        credit = JournalEntry.objects.filter(account=account, journal__posted=True, journal__approved=True).aggregate(Sum('credit'))['credit__sum'] or 0
        balance = debit - credit if account.type in ['asset', 'expense'] else credit - debit
        rows.append({'account': account, 'debit': debit, 'credit': credit, 'balance': balance})
        total_debit += debit
        total_credit += credit
    return render(request, 'accounting/trial_balance.html', {'rows': rows, 'total_debit': total_debit, 'total_credit': total_credit})

def income_statement(request):
    accounts = Account.objects.filter(type__in=['income', 'expense'], active=True).order_by('account_code')
    period_start = request.GET.get('start', '')
    period_end = request.GET.get('end', '')
    entries = JournalEntry.objects.filter(account__in=accounts, journal__posted=True, journal__approved=True)
    if period_start:
        entries = entries.filter(journal__date__gte=period_start)
    if period_end:
        entries = entries.filter(journal__date__lte=period_end)
    income = 0
    expense = 0
    rows = []
    for account in accounts:
        acc_entries = entries.filter(account=account)
        debit = acc_entries.aggregate(Sum('debit'))['debit__sum'] or 0
        credit = acc_entries.aggregate(Sum('credit'))['credit__sum'] or 0
        balance = credit - debit if account.type == 'income' else debit - credit
        rows.append({'account': account, 'balance': balance})
        if account.type == 'income':
            income += balance
        else:
            expense += balance
    net_income = income - expense
    return render(request, 'accounting/income_statement.html', {'rows': rows, 'income': income, 'expense': expense, 'net_income': net_income, 'period_start': period_start, 'period_end': period_end})

def general_ledger_report(request):
    accounts = Account.objects.filter(active=True).order_by('account_code')
    period_start = request.GET.get('start', '')
    period_end = request.GET.get('end', '')
    ledgers = []
    for account in accounts:
        entries = account.get_ledger_entries().filter(journal__posted=True, journal__approved=True)
        if period_start:
            entries = entries.filter(journal__date__gte=period_start)
        if period_end:
            entries = entries.filter(journal__date__lte=period_end)
        ledgers.append({'account': account, 'entries': entries})
    return render(request, 'accounting/general_ledger.html', {'ledgers': ledgers, 'period_start': period_start, 'period_end': period_end})

def cash_flow_statement(request):
    # Simple cash flow: sum all cash/bank account movements
    cash_accounts = Account.objects.filter(type='asset', name__icontains='cash') | Account.objects.filter(type='asset', name__icontains='bank')
    period_start = request.GET.get('start', '')
    period_end = request.GET.get('end', '')
    entries = JournalEntry.objects.filter(account__in=cash_accounts, journal__posted=True, journal__approved=True)
    if period_start:
        entries = entries.filter(journal__date__gte=period_start)
    if period_end:
        entries = entries.filter(journal__date__lte=period_end)
    inflow = entries.aggregate(Sum('debit'))['debit__sum'] or 0
    outflow = entries.aggregate(Sum('credit'))['credit__sum'] or 0
    net_cash = inflow - outflow
    return render(request, 'accounting/cash_flow.html', {'inflow': inflow, 'outflow': outflow, 'net_cash': net_cash, 'period_start': period_start, 'period_end': period_end})

def journal_report(request):
    journals = Journal.objects.all().order_by('-date')
    journal_type = request.GET.get('type', '')
    approved = request.GET.get('approved', '')
    posted = request.GET.get('posted', '')
    if journal_type:
        journals = journals.filter(journal_type=journal_type)
    if approved:
        journals = journals.filter(approved=(approved == '1'))
    if posted:
        journals = journals.filter(posted=(posted == '1'))
    return render(request, 'accounting/journal_report.html', {'journals': journals})
