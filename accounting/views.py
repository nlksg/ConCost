from django.shortcuts import render, redirect, get_object_or_404
from .models import Journal, CapitalContribution, JournalEntry
from .forms import JournalForm, JournalEntryFormSet, CapitalContributionForm
from .views_ledger import account_ledger
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils import timezone

def index(request):
    if not request.user.is_authenticated:
        return render(request, 'accounting/welcome.html')
    return render(request, 'accounting/index.html')

@login_required
def journal_list(request):
    journals = Journal.objects.select_related('site').all().order_by('-date')
    return render(request, 'accounting/transaction_list.html', {'transactions': journals, 'is_approver': is_approver(request.user)})

@login_required
def journal_create(request):
    if request.method == 'POST':
        form = JournalForm(request.POST)
        formset = JournalEntryFormSet(request.POST)
        if form.is_valid() and formset.is_valid():
            journal = form.save(commit=False)
            journal.posted = False  # Always save as draft first
            journal.save()
            entries = formset.save(commit=False)
            for entry in entries:
                entry.journal = journal
                entry.save()
            return redirect('accounting:transaction_list')
    else:
        form = JournalForm()
        formset = JournalEntryFormSet()
    return render(request, 'accounting/transaction_form.html', {'form': form, 'formset': formset})

@login_required
def journal_post(request, pk):
    journal = get_object_or_404(Journal, pk=pk)
    if request.method == 'POST':
        if not is_approver(request.user):
            return render(request, 'accounting/transaction_post.html', {'transaction': journal, 'error': 'You do not have permission to approve or lock this journal.'})
        if not journal.is_balanced():
            error = 'Journal is not balanced. Cannot post.'
            return render(request, 'accounting/transaction_post.html', {'transaction': journal, 'error': error})
        if 'approve' in request.POST:
            journal.approved = True
            journal.approved_by = request.user.get_full_name() or request.user.username
            journal.approved_at = timezone.now()
            journal.locked = True
            journal.posted = True
            journal.save()
            return redirect('accounting:journal_list')
        elif 'lock' in request.POST:
            journal.locked = True
            journal.save()
            return redirect('accounting:journal_list')
    return render(request, 'accounting/transaction_post.html', {'transaction': journal, 'is_approver': is_approver(request.user)})

@login_required
def capital_contribution_list(request):
    contributions = CapitalContribution.objects.select_related('shareholder').order_by('-date')
    return render(request, 'accounting/capital_contribution_list.html', {'contributions': contributions})

@login_required
def capital_contribution_create(request):
    from .models import Account, JournalEntry
    if request.method == 'POST':
        form = CapitalContributionForm(request.POST)
        if form.is_valid():
            contribution = form.save(commit=False)
            # Find accounts
            try:
                cash_account = Account.objects.get(account_code="1000")  # Cash
            except Account.DoesNotExist:
                cash_account = Account.objects.filter(type='asset').first()
            try:
                capital_account = Account.objects.get(account_code="3000")  # Share Capital
            except Account.DoesNotExist:
                capital_account = Account.objects.filter(type='equity').first()
            # Create journal
            journal = Journal.objects.create(
                description=f"Capital contribution by {contribution.shareholder.name}",
                date=contribution.date,
                posted=True
            )
            JournalEntry.objects.create(journal=journal, account=cash_account, debit=contribution.amount, credit=0)
            JournalEntry.objects.create(journal=journal, account=capital_account, debit=0, credit=contribution.amount)
            contribution.journal = journal
            contribution.save()
            return redirect('accounting:capital_contribution_list')
    else:
        form = CapitalContributionForm()
    return render(request, 'accounting/capital_contribution_form.html', {'form': form})

@login_required
def balance_sheet(request):
    from .models import Account, JournalEntry
    # Calculate balances for each account
    accounts = Account.objects.all().order_by('account_code')
    balances = []
    for account in accounts:
        debit = sum(e.debit for e in JournalEntry.objects.filter(account=account, journal__posted=True, journal__approved=True))
        credit = sum(e.credit for e in JournalEntry.objects.filter(account=account, journal__posted=True, journal__approved=True))
        balance = debit - credit if account.type in ['asset', 'expense'] else credit - debit
        balances.append({
            'account': account,
            'balance': balance
        })
    # Group by type
    assets = [b for b in balances if b['account'].type == 'asset']
    liabilities = [b for b in balances if b['account'].type == 'liability']
    equity = [b for b in balances if b['account'].type == 'equity']
    total_assets = sum(b['balance'] for b in assets)
    total_liabilities = sum(b['balance'] for b in liabilities)
    total_equity = sum(b['balance'] for b in equity)
    return render(request, 'accounting/balance_sheet.html', {
        'assets': assets,
        'liabilities': liabilities,
        'equity': equity,
        'total_assets': total_assets,
        'total_liabilities': total_liabilities,
        'total_equity': total_equity,
    })

def is_approver(user):
    return user.is_superuser or user.groups.filter(name__in=["Admin", "Accountant"]).exists()

def is_site_owner(user):
    return user.groups.filter(name="Site Owner").exists()
