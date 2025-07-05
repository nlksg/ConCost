from django.contrib import admin
from .models import Purchase, PurchaseLine, Item

class PurchaseLineInline(admin.TabularInline):
    model = PurchaseLine
    extra = 1

@admin.register(Purchase)
class PurchaseAdmin(admin.ModelAdmin):
    list_display = ('id', 'site', 'description', 'date', 'approved')
    inlines = [PurchaseLineInline]

@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'item_type', 'expense_account', 'unit_of_measure')
    list_filter = ('item_type',)
    search_fields = ('name', 'description')
