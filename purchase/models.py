from django.db import models
from django.contrib.auth.models import User
from accounting.models import Journal, Account, ConstructionSite
from SiteExpense.models import SiteExpense

class Item(models.Model):
    """
    Represents a purchasable material or service.
    """
    ITEM_TYPE_CHOICES = [
        ('material', 'Material'),
        ('service', 'Service'),
    ]
    name = models.CharField(max_length=200, unique=True)
    description = models.TextField(blank=True)
    item_type = models.CharField(max_length=20, choices=ITEM_TYPE_CHOICES, default='material')
    unit_of_measure = models.CharField(max_length=50, blank=True, help_text="e.g., kg, hour, piece")
    expense_account = models.ForeignKey(Account, on_delete=models.PROTECT,
                                        help_text="Default expense account for this item.")

    def __str__(self):
        return self.name

class Purchase(models.Model):
    site = models.ForeignKey(ConstructionSite, on_delete=models.CASCADE)
    site_expense = models.OneToOneField(SiteExpense, on_delete=models.SET_NULL, null=True, blank=True, related_name='purchase')
    date = models.DateField()
    description = models.CharField(max_length=255)
    approved = models.BooleanField(default=False)
    journal = models.OneToOneField(Journal, on_delete=models.SET_NULL, null=True, blank=True, related_name='purchase')
    created_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name='purchases_created')
    approved_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name='purchases_approved', null=True, blank=True)
    approved_at = models.DateTimeField(null=True, blank=True)
    accounts_payable_account = models.ForeignKey(Account, on_delete=models.PROTECT, null=True, blank=True, related_name='purchases_as_ap', help_text='Default: Accounts Payable')

    def __str__(self):
        return f"Purchase {self.id} - {self.description}"

class PurchaseLine(models.Model):
    purchase = models.ForeignKey(Purchase, on_delete=models.CASCADE, related_name='lines')
    item = models.ForeignKey(Item, on_delete=models.PROTECT)
    description = models.CharField(max_length=255, help_text="Editable description for this specific purchase.")
    quantity = models.DecimalField(max_digits=12, decimal_places=2, default=1)
    unit_price = models.DecimalField(max_digits=12, decimal_places=2)

    @property
    def total(self):
        """Calculates the total amount for the line."""
        return self.quantity * self.unit_price

    def __str__(self):
        return f"{self.quantity} x {self.item.name} @ {self.unit_price}"
