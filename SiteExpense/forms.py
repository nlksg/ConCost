from django import forms
from .models import SiteExpense

class SiteExpenseForm(forms.ModelForm):
    class Meta:
        model = SiteExpense
        fields = ['site', 'description', 'amount', 'date', 'receipt']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }
