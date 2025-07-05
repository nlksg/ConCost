from django import forms
from .models import Journal, JournalEntry, CapitalContribution, Account
from django.forms import ModelForm, inlineformset_factory

class JournalForm(ModelForm):
    date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    class Meta:
        model = Journal
        fields = ['description', 'date', 'site']

JournalEntryFormSet = inlineformset_factory(
    Journal, JournalEntry,
    fields=['account', 'debit', 'credit'],
    extra=2,  # At least two entries for double-entry
    can_delete=False
)

class CapitalContributionForm(ModelForm):
    date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    class Meta:
        model = CapitalContribution
        fields = ['shareholder', 'amount', 'date']

class AccountForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ['name', 'account_code', 'type', 'parent', 'active']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['parent'].queryset = Account.objects.order_by('name')
