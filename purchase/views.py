import json
from django.db import models
from django.shortcuts import render, get_object_or_404, redirect
from .models import Purchase, PurchaseLine, Item
from .forms import PurchaseForm, PurchaseLineFormSet, ItemForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils import timezone
from accounting.models import Journal, JournalEntry, Account
from django.contrib import messages
from SiteExpense.models import SiteExpense # Import SiteExpense

def is_accountant_or_admin(user):
    return user.groups.filter(name__in=['Accountant', 'Admin']).exists()

def get_item_data_json():
    """Returns a JSON string of all items for use in JavaScript."""
    items = Item.objects.all()
    item_data = {
        item.pk: {
            'description': item.description,
            'unit_price': str(item.unit_price) # Use string to avoid JSON issues with Decimal
        } for item in items
    }
    return json.dumps(item_data)

@login_required
def purchase_list(request):
    purchases = Purchase.objects.all().order_by('-date')
    return render(request, 'purchase/purchase_list.html', {'purchases': purchases})

@user_passes_test(is_accountant_or_admin)
def purchase_create(request):
    site_expense_id = request.GET.get('site_expense') or request.POST.get('site_expense')
    site_expense = None
    if site_expense_id:
        site_expense = get_object_or_404(SiteExpense, pk=site_expense_id)

    if request.method == 'POST':
        form = PurchaseForm(request.POST)
        formset = PurchaseLineFormSet(request.POST)
        if form.is_valid() and formset.is_valid():
            purchase = form.save(commit=False)
            purchase.created_by = request.user
            if site_expense:
                purchase.site_expense = site_expense
            purchase.save()
            formset.instance = purchase
            formset.save()
            
            if site_expense:
                site_expense.purchase = purchase
                site_expense.save()

            return redirect('purchase:purchase_list')
    else:
        initial_data = {}
        if site_expense:
            initial_data = {
                'description': f"From Site Expense: {site_expense.description}",
                'date': site_expense.date,
                'site': site_expense.site,
                'site_expense': site_expense.pk,
            }

        form = PurchaseForm(initial=initial_data)
        formset = PurchaseLineFormSet()

    return render(request, 'purchase/purchase_form.html', {
        'form': form,
        'formset': formset,
        'site_expense': site_expense
    })

@login_required
def purchase_edit(request, pk):
    purchase = get_object_or_404(Purchase, pk=pk)
    if request.method == 'POST':
        form = PurchaseForm(request.POST, instance=purchase)
        formset = PurchaseLineFormSet(request.POST, instance=purchase)
        if form.is_valid() and formset.is_valid():
            form.save()
            formset.save()
            return redirect('purchase:purchase_list')
    else:
        form = PurchaseForm(instance=purchase)
        formset = PurchaseLineFormSet(instance=purchase)
    return render(request, 'purchase/purchase_form.html', {
        'form': form, 
        'formset': formset, 
        'purchase': purchase,
        'item_data_json': get_item_data_json()
    })

@user_passes_test(is_accountant_or_admin)
def approve_purchase(request, pk):
    purchase = get_object_or_404(Purchase, pk=pk)
    if not purchase.approved:
        # Use selected AP account or default
        ap_account = purchase.accounts_payable_account
        if not ap_account:
            try:
                # Try to get the default 'Accounts Payable' account
                ap_account = Account.objects.get(account_code="2000")
            except Account.DoesNotExist:
                messages.error(request, "No default Accounts Payable account (code 2000) found. Please create one or select an account on the purchase.")
                return redirect('purchase:purchase_edit', pk=purchase.pk)

        # Create Journal
        journal = Journal.objects.create(
            description=f"Purchase #{purchase.pk}: {purchase.description}",
            date=purchase.date,
            site=purchase.site,
            journal_type='purchase',
            created_by=request.user,
            posted=True, # Journals from purchases are auto-posted
            approved=True,
            approved_by=request.user,
            approved_at=timezone.now(),
            locked=True,
        )
        
        grand_total = 0
        for line in purchase.lines.all():
            if line.item and line.item.expense_account:
                JournalEntry.objects.create(
                    journal=journal,
                    account=line.item.expense_account, # Use account from item
                    debit=line.total, # Use the calculated total property
                    credit=0,
                    description=f"Item: {line.item.name}"
                )
                grand_total += line.total
            else:
                # Handle case where an item or its expense account is missing
                messages.error(request, f"Line item '{line.description}' is missing an item or the item has no expense account linked.")
                journal.delete() # Rollback journal creation
                return redirect('purchase:purchase_edit', pk=purchase.pk)

        if grand_total > 0:
            JournalEntry.objects.create(
                journal=journal,
                account=ap_account,
                debit=0,
                credit=grand_total
            )
        else:
            # If total is zero, no need for a journal.
            journal.delete()
            messages.warning(request, "Purchase total is zero. No journal entry was created.")
            return redirect('purchase:purchase_list')

        purchase.journal = journal
        purchase.approved = True
        purchase.approved_by = request.user
        purchase.approved_at = timezone.now()
        purchase.save()

        if purchase.site_expense:
            purchase.site_expense.status = 'approved'
            purchase.site_expense.save()

        messages.success(request, f"Purchase #{purchase.pk} approved and Journal #{journal.pk} created.")
    else:
        messages.info(request, f"Purchase #{purchase.pk} has already been approved.")
        
    return redirect('purchase:purchase_list')

# Item (Catalog) Views
# =======================

@user_passes_test(is_accountant_or_admin)
def item_list(request):
    items = Item.objects.all().order_by('name')
    return render(request, 'purchase/item_list.html', {'items': items})

@user_passes_test(is_accountant_or_admin)
def item_create(request):
    if request.method == 'POST':
        form = ItemForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Item created successfully.")
            return redirect('purchase:item_list')
    else:
        form = ItemForm()
    return render(request, 'purchase/item_form.html', {'form': form})

@user_passes_test(is_accountant_or_admin)
def item_edit(request, pk):
    item = get_object_or_404(Item, pk=pk)
    if request.method == 'POST':
        form = ItemForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            messages.success(request, "Item updated successfully.")
            return redirect('purchase:item_list')
    else:
        form = ItemForm(instance=item)
    return render(request, 'purchase/item_form.html', {'form': form, 'item': item})

@user_passes_test(is_accountant_or_admin)
def item_delete(request, pk):
    item = get_object_or_404(Item, pk=pk)
    if request.method == 'POST':
        try:
            item.delete()
            messages.success(request, "Item deleted successfully.")
            return redirect('purchase:item_list')
        except models.ProtectedError as e:
            messages.error(request, f"Cannot delete this item because it is used in one or more purchases. {e}")
            return redirect('purchase:item_list')
    return render(request, 'purchase/item_confirm_delete.html', {'item': item})
