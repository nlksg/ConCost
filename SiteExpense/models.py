from django.db import models
from accounting.models import ConstructionSite

# Create your models here.

class SiteExpense(models.Model):
    site = models.ForeignKey(ConstructionSite, on_delete=models.CASCADE)
    description = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    date = models.DateField()
    submitted_by = models.CharField(max_length=100)
    receipt = models.ImageField(upload_to='site_expenses/', null=True, blank=True)
    approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.site} - {self.description} ({self.amount})"
