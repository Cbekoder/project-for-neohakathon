from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from companies.models import Company
from properties.models import Property
from news.models import NewsArticle
from chat.models import ChatRoom, ChatMessage, Appointment

User = get_user_model()

class Command(BaseCommand):
    help = 'Clear all data from database (except superusers)'

    def add_arguments(self, parser):
        parser.add_argument(
            '--confirm',
            action='store_true',
            help='Confirm deletion of all data',
        )

    def handle(self, *args, **options):
        if not options['confirm']:
            self.stdout.write(
                self.style.WARNING(
                    'This will delete ALL data from the database (except superusers).\n'
                    'Use --confirm flag to proceed.'
                )
            )
            return

        self.stdout.write('Clearing database...')

        # Delete in order to avoid foreign key constraints
        ChatMessage.objects.all().delete()
        ChatRoom.objects.all().delete()
        Appointment.objects.all().delete()
        NewsArticle.objects.all().delete()
        Property.objects.all().delete()
        Company.objects.all().delete()
        
        # Delete non-superuser users
        User.objects.filter(is_superuser=False).delete()

        self.stdout.write(
            self.style.SUCCESS('Database cleared successfully!')
        )
