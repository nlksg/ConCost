from django.shortcuts import render, redirect
from .forms import SiteExpenseForm
from .models import SiteExpense
from django.contrib.auth.decorators import login_required

@login_required
def expense_list(request):
    expenses = SiteExpense.objects.all().order_by('-created_at')
    return render(request, 'siteexpense/expense_list.html', {'expenses': expenses})

@login_required
def submit_expense(request):
    if request.method == 'POST':
        form = SiteExpenseForm(request.POST, request.FILES)
        if form.is_valid():
            expense = form.save(commit=False)
            expense.submitted_by = request.user.get_username()
            expense.save()
            return redirect('siteexpense:expense_submitted')
    else:
        form = SiteExpenseForm()
    return render(request, 'siteexpense/submit_expense.html', {'form': form})

@login_required
def expense_submitted(request):
    return render(request, 'siteexpense/expense_submitted.html')
