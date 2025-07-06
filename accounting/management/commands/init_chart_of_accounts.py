from django.core.management.base import BaseCommand
from accounting.models import Account

class Command(BaseCommand):
    help = 'Initializes a default chart of accounts for the company.'

    DEFAULT_ACCOUNTS = [
        # Assets
        {'name': 'Cash', 'code': '1000', 'type': 'asset'},
        {'name': 'Accounts Receivable', 'code': '1100', 'type': 'asset'},
        {'name': 'Inventory', 'code': '1200', 'type': 'asset'},
        # Liabilities
        {'name': 'Accounts Payable', 'code': '2000', 'type': 'liability'},
        {'name': 'Loans Payable', 'code': '2100', 'type': 'liability'},
        # Equity
        {'name': 'Owner Equity', 'code': '3000', 'type': 'equity'},
        {'name': 'Retained Earnings', 'code': '3100', 'type': 'equity'},
        # Revenue
        {'name': 'Construction Revenue', 'code': '4000', 'type': 'revenue'},
        # Expenses
        {'name': 'Materials Expense', 'code': '5000', 'type': 'expense'},
        {'name': 'Labor Expense', 'code': '5100', 'type': 'expense'},
        {'name': 'Subcontractor Expense', 'code': '5200', 'type': 'expense'},
        {'name': 'Equipment Rental Expense', 'code': '5300', 'type': 'expense'},
        {'name': 'Site Overhead Expense', 'code': '5400', 'type': 'expense'},
        {'name': 'Other Expense', 'code': '5900', 'type': 'expense'},
    ]

    def handle(self, *args, **options):
        created = 0
        for acc in self.DEFAULT_ACCOUNTS:
            obj, was_created = Account.objects.get_or_create(
                account_code=acc['code'],
                defaults={
                    'name': acc['name'],
                    'type': acc['type'],
                    'active': True
                }
            )
            if was_created:
                created += 1
                self.stdout.write(self.style.SUCCESS(f"Created account: {acc['code']} - {acc['name']}"))
            else:
                self.stdout.write(f"Account already exists: {acc['code']} - {acc['name']}")
        self.stdout.write(self.style.SUCCESS(f"Initialization complete. {created} new accounts created."))
