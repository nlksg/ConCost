from django import forms
from .models import Purchase, PurchaseLine, Item

class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['name', 'description', 'item_type', 'unit_of_measure', 'expense_account']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        from accounting.models import Account  # Lazy import
        qs = Account.objects.filter(type='expense').order_by('name')
        # If editing, ensure the current value is included even if not in qs
        if self.instance and self.instance.pk and self.instance.expense_account:
            current = Account.objects.filter(pk=self.instance.expense_account.pk)
            qs = (qs | current).distinct()
        self.fields['expense_account'].queryset = qs

class PurchaseForm(forms.ModelForm):
    class Meta:
        model = Purchase
        fields = ['site', 'site_expense', 'date', 'description', 'accounts_payable_account']
        # Note: 'approved' is intentionally removed from this form.

class PurchaseLineForm(forms.ModelForm):
    class Meta:
        model = PurchaseLine
        fields = ['item', 'description', 'quantity', 'unit_price']

PurchaseLineFormSet = forms.inlineformset_factory(
    Purchase, PurchaseLine,
    form=PurchaseLineForm,
    extra=1,
    can_delete=True
)
