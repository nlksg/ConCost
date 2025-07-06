from django.core.management.base import BaseCommand
from django.apps import apps

class Command(BaseCommand):
    help = 'Purges all transactional data from the database, leaving users and groups intact.'

    def handle(self, *args, **options):
        # List of models to purge
        models_to_purge = [
            'SiteExpense.SiteExpense',
            'purchase.PurchaseLine',
            'purchase.Purchase',
            'purchase.Item',
            'accounting.JournalEntry',
            'accounting.Journal',
            'accounting.CapitalContribution',
            'accounting.ConstructionSite',
            'accounting.Account',
        ]

        self.stdout.write(self.style.WARNING('Starting data purge...'))

        for model_name in models_to_purge:
            try:
                Model = apps.get_model(model_name)
                count, _ = Model.objects.all().delete()
                self.stdout.write(self.style.SUCCESS(f'Successfully deleted {count} objects from {model_name}'))
            except LookupError:
                self.stdout.write(self.style.ERROR(f'Model {model_name} not found.'))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'Error purging {model_name}: {e}'))

        self.stdout.write(self.style.SUCCESS('Data purge complete.'))
