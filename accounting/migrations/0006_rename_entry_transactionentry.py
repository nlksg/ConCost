# Generated by Django 5.2.4 on 2025-07-03 19:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounting', '0005_capitalcontribution_transaction'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Entry',
            new_name='TransactionEntry',
        ),
    ]
