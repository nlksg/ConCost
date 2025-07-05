from django.db import migrations

def create_standard_accounts(apps, schema_editor):
    Account = apps.get_model('accounting', 'Account')
    standard_accounts = [
        # Assets
        ("1000", "Cash", "asset"),
        ("1100", "Accounts Receivable", "asset"),
        ("1200", "Inventory", "asset"),
        ("1300", "Prepaid Expenses", "asset"),
        ("1400", "Property, Plant, and Equipment", "asset"),
        # Liabilities
        ("2000", "Accounts Payable", "liability"),
        ("2100", "Accrued Expenses", "liability"),
        ("2200", "Notes Payable", "liability"),
        # Equity
        ("3000", "Share Capital", "equity"),
        ("3100", "Retained Earnings", "equity"),
        # Income
        ("4000", "Construction Revenue", "income"),
        ("4100", "Other Income", "income"),
        # Expenses
        ("5000", "Material Expense", "expense"),
        ("5100", "Labor Expense", "expense"),
        ("5200", "Overhead Expense", "expense"),
        ("5300", "Depreciation Expense", "expense"),
        ("5400", "Other Expense", "expense"),
    ]
    for code, name, acc_type in standard_accounts:
        Account.objects.get_or_create(account_code=code, defaults={"name": name, "type": acc_type})

class Migration(migrations.Migration):
    dependencies = [
        ("accounting", "0002_account_account_code"),
    ]
    operations = [
        migrations.RunPython(create_standard_accounts),
    ]
