from django.db import models

# Create your models here.

class ShareHolder(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(blank=True)

    def __str__(self):
        return self.name

class CapitalContribution(models.Model):
    shareholder = models.ForeignKey(ShareHolder, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    date = models.DateField()
    journal = models.ForeignKey('Journal', on_delete=models.CASCADE, null=True, blank=True, related_name='capital_contributions')

    def __str__(self):
        return f"{self.shareholder.name} - {self.amount}"

class ConstructionSite(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class Account(models.Model):
    ACCOUNT_TYPES = [
        ('asset', 'Asset'),
        ('liability', 'Liability'),
        ('equity', 'Equity'),
        ('income', 'Income'),
        ('expense', 'Expense'),
    ]
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=10, choices=ACCOUNT_TYPES)
    account_code = models.CharField(max_length=20, unique=True)
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL, related_name='children')
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    def get_ledger_entries(self):
        """Return all JournalEntries for this account, ordered by date and journal id."""
        return JournalEntry.objects.filter(account=self).select_related('journal').order_by('journal__date', 'journal__id')

    def get_ledger_url(self):
        from django.urls import reverse
        return reverse('accounting:account_ledger', args=[self.pk])

class Journal(models.Model):
    description = models.CharField(max_length=200)
    date = models.DateField()
    site = models.ForeignKey(ConstructionSite, on_delete=models.SET_NULL, null=True, blank=True, help_text="Leave blank for company-wide transactions.")
    posted = models.BooleanField(default=False)
    JOURNAL_TYPES = [
        ('general', 'General'),
        ('cash_receipts', 'Cash Receipts'),
        ('cash_payments', 'Cash Payments'),
        ('sales', 'Sales'),
        ('purchases', 'Purchases'),
        ('bank', 'Bank'),
        ('petty_cash', 'Petty Cash'),
        ('payroll', 'Payroll'),
        ('capital', 'Capital'),
        ('adjustment', 'Adjustment'),
    ]
    journal_type = models.CharField(max_length=20, choices=JOURNAL_TYPES, default='general')
    approved = models.BooleanField(default=False)
    approved_by = models.CharField(max_length=100, null=True, blank=True)
    approved_at = models.DateTimeField(null=True, blank=True)
    locked = models.BooleanField(default=False)

    def is_balanced(self):
        total_debit = sum(entry.debit for entry in self.entries.all())
        total_credit = sum(entry.credit for entry in self.entries.all())
        return total_debit == total_credit

    def __str__(self):
        if self.site:
            return f"{self.date} - {self.get_journal_type_display()} - {self.description} ({self.site.name})"
        return f"{self.date} - {self.get_journal_type_display()} - {self.description} (Company-wide)"

class JournalEntry(models.Model):
    journal = models.ForeignKey(Journal, related_name='entries', on_delete=models.CASCADE)
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    debit = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    credit = models.DecimalField(max_digits=15, decimal_places=2, default=0)

    def __str__(self):
        return f"{self.account.name}: Debit {self.debit} / Credit {self.credit}"
