from django.contrib import admin
from .models import ShareHolder, CapitalContribution, ConstructionSite, Account, Journal, JournalEntry

class AccountAdmin(admin.ModelAdmin):
    list_display = ('account_code', 'name', 'type', 'parent', 'active')
    list_filter = ('type', 'active')
    search_fields = ('account_code', 'name')
    list_editable = ('active',)

admin.site.register(ShareHolder)
admin.site.register(CapitalContribution)
admin.site.register(ConstructionSite)
admin.site.register(Account, AccountAdmin)
admin.site.register(Journal)
admin.site.register(JournalEntry)
