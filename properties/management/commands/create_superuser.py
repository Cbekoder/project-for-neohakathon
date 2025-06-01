from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from companies.models import Company

User = get_user_model()

class Command(BaseCommand):
    help = 'Create a superuser with sample company'

    def add_arguments(self, parser):
        parser.add_argument('--username', type=str, help='Username for superuser', default='admin')
        parser.add_argument('--email', type=str, help='Email for superuser', default='admin@realestate.uz')
        parser.add_argument('--password', type=str, help='Password for superuser', default='admin123')

    def handle(self, *args, **options):
        username = options['username']
        email = options['email']
        password = options['password']

        if User.objects.filter(username=username).exists():
            self.stdout.write(
                self.style.WARNING(f'User {username} already exists')
            )
            return

        # Create superuser
        user = User.objects.create_superuser(
            username=username,
            email=email,
            password=password,
            user_type='admin'
        )

        # Create a company for the superuser
        company = Company.objects.create(
            name='Ko\'chmas Mulk Pro Admin',
            company_type='realtor',
            description='Platform administratori kompaniyasi',
            address='Admin ko\'chasi 1, Toshkent',
            phone='+998 90 000 00 00',
            email=email,
            website='https://kochmmasmulkpro.uz',
            license_number='ADMIN-2024-001',
            founded_year=2024,
            rating=5.0,
            total_sales=0,
            active_properties=0,
            is_verified=True
        )

        user.company = company
        user.save()

        self.stdout.write(
            self.style.SUCCESS(f'Successfully created superuser: {username}')
        )
        self.stdout.write(
            self.style.SUCCESS(f'Company created: {company.name}')
        )
        self.stdout.write(
            self.style.SUCCESS(f'Login credentials: {username} / {password}')
        )
