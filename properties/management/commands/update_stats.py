from django.core.management.base import BaseCommand
from django.db.models import Count, Sum
from companies.models import Company
from properties.models import Property

class Command(BaseCommand):
    help = 'Update company statistics based on their properties'

    def handle(self, *args, **options):
        self.stdout.write('Updating company statistics...')
        
        companies = Company.objects.all()
        
        for company in companies:
            # Update active properties count
            active_properties = company.properties.filter(status='active').count()
            
            # Update total sales (sold properties)
            total_sales = company.properties.filter(status='sold').count()
            
            # Update total views
            total_views = company.properties.aggregate(
                total=Sum('views_count')
            )['total'] or 0
            
            company.active_properties = active_properties
            company.total_sales = total_sales
            company.save()
            
            self.stdout.write(
                f'Updated {company.name}: {active_properties} active, {total_sales} sales'
            )
        
        self.stdout.write(
            self.style.SUCCESS('Company statistics updated successfully!')
        )
