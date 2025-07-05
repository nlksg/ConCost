from django.shortcuts import render, get_object_or_404, redirect
from .models import Account
from .forms import AccountForm
from django.contrib.auth.decorators import login_required

@login_required
def account_ledger(request, pk):
    account = get_object_or_404(Account, pk=pk)
    entries = account.get_ledger_entries()
    # Calculate running balance
    balance = 0
    running_balances = []
    for entry in entries:
        if account.type in ['asset', 'expense']:
            balance += entry.debit - entry.credit
        else:
            balance += entry.credit - entry.debit
        running_balances.append(balance)
    entry_data = zip(entries, running_balances)
    return render(request, 'accounting/account_ledger.html', {
        'account': account,
        'entry_data': entry_data,
    })


def build_account_tree(accounts):
    account_dict = {a.pk: a for a in accounts}
    tree = []
    children = {a.pk: [] for a in accounts}
    for a in accounts:
        if a.parent_id:
            children[a.parent_id].append(a)
        else:
            tree.append(a)
    def attach_children(node):
        node._children = children[node.pk]
        for child in node._children:
            attach_children(child)
    for root in tree:
        attach_children(root)
    return tree

@login_required
def account_list(request):
    accounts = Account.objects.all().order_by('account_code')
    parents = Account.objects.filter(parent__isnull=True)
    code = request.GET.get('code', '').strip()
    name = request.GET.get('name', '').strip()
    type_ = request.GET.get('type', '')
    parent = request.GET.get('parent', '')
    active = request.GET.get('active', '')
    if code:
        accounts = accounts.filter(account_code__icontains=code)
    if name:
        accounts = accounts.filter(name__icontains=name)
    if type_:
        accounts = accounts.filter(type=type_)
    if parent:
        accounts = accounts.filter(parent__pk=parent)
    if active != '':
        accounts = accounts.filter(active=(active == '1'))
    account_tree = build_account_tree(accounts)
    return render(request, 'accounting/account_list.html', {'accounts': accounts, 'parents': parents, 'account_tree': account_tree})

@login_required
def account_create(request):
    parent_id = request.GET.get('parent')
    if request.method == 'POST':
        form = AccountForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('accounting:account_list')
    else:
        initial_data = {}
        if parent_id:
            initial_data['parent'] = parent_id
        form = AccountForm(initial=initial_data)
    return render(request, 'accounting/account_form.html', {'form': form})

@login_required
def account_edit(request, pk):
    account = get_object_or_404(Account, pk=pk)
    if request.method == 'POST':
        form = AccountForm(request.POST, instance=account)
        if form.is_valid():
            form.save()
            return redirect('accounting:account_list')
    else:
        form = AccountForm(instance=account)
    return render(request, 'accounting/account_form.html', {'form': form, 'account': account})
