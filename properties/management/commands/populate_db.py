import random
from decimal import Decimal
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import datetime, timedelta
from companies.models import Company, CompanySpecialty, CompanyTeamMember
from properties.models import Property, PropertyImage, PropertyAmenity
from news.models import NewsArticle
from accounts.models import UserProfile

User = get_user_model()

class Command(BaseCommand):
    help = 'Populate database with sample data'

    def add_arguments(self, parser):
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Clear existing data before populating',
        )

    def handle(self, *args, **options):
        if options['clear']:
            self.stdout.write('Clearing existing data...')
            Property.objects.all().delete()
            Company.objects.all().delete()
            User.objects.filter(is_superuser=False).delete()
            NewsArticle.objects.all().delete()
            self.stdout.write(self.style.SUCCESS('Data cleared successfully'))

        self.stdout.write('Starting database population...')
        
        # Create users
        self.create_users()
        
        # Create companies
        self.create_companies()
        
        # Create properties
        self.create_properties()
        
        # Create news articles
        self.create_news()
        
        self.stdout.write(self.style.SUCCESS('Database populated successfully!'))

    def create_users(self):
        self.stdout.write('Creating users...')
        
        # Create admin users
        admin_users = [
            {
                'username': 'admin_john',
                'email': 'john@eliterealty.com',
                'first_name': 'John',
                'last_name': 'Smith',
                'user_type': 'admin',
                'password': 'password123'
            },
            {
                'username': 'agent_sarah',
                'email': 'sarah@premiumprops.com',
                'first_name': 'Sarah',
                'last_name': 'Johnson',
                'user_type': 'agent',
                'password': 'password123'
            },
            {
                'username': 'seller_mike',
                'email': 'mike@buildright.com',
                'first_name': 'Mike',
                'last_name': 'Wilson',
                'user_type': 'seller',
                'password': 'password123'
            }
        ]
        
        # Create buyer users
        buyer_users = [
            {
                'username': 'buyer_alex',
                'email': 'alex@email.com',
                'first_name': 'Alex',
                'last_name': 'Brown',
                'user_type': 'buyer',
                'password': 'password123'
            },
            {
                'username': 'buyer_emma',
                'email': 'emma@email.com',
                'first_name': 'Emma',
                'last_name': 'Davis',
                'user_type': 'buyer',
                'password': 'password123'
            },
            {
                'username': 'buyer_james',
                'email': 'james@email.com',
                'first_name': 'James',
                'last_name': 'Miller',
                'user_type': 'buyer',
                'password': 'password123'
            }
        ]
        
        all_users = admin_users + buyer_users
        
        for user_data in all_users:
            if not User.objects.filter(username=user_data['username']).exists():
                user = User.objects.create_user(
                    username=user_data['username'],
                    email=user_data['email'],
                    first_name=user_data['first_name'],
                    last_name=user_data['last_name'],
                    user_type=user_data['user_type'],
                    password=user_data['password']
                )
                
                # Create user profile
                UserProfile.objects.create(
                    user=user,
                    bio=f"Professional {user_data['user_type']} with years of experience",
                    location="Toshkent, O'zbekiston",
                    budget_min=Decimal('200000') if user_data['user_type'] == 'buyer' else None,
                    budget_max=Decimal('800000') if user_data['user_type'] == 'buyer' else None,
                    preferred_locations="Shahar markazi, Chilonzor, Yunusobod"
                )
                
                self.stdout.write(f'Created user: {user.username}')

    def create_companies(self):
        self.stdout.write('Creating companies...')
        
        companies_data = [
            {
                'name': 'Elite Realty Group',
                'company_type': 'realtor',
                'description': '20 yildan ortiq tajribaga ega hashamatli mulklar bo\'yicha premium ko\'chmas mulk xizmatlari.',
                'address': '123 Business Ave, Shahar markazi, Toshkent',
                'phone': '+998 90 123 45 67',
                'email': 'contact@eliterealty.uz',
                'website': 'https://eliterealty.uz',
                'license_number': 'RE-2024-001234',
                'founded_year': 2004,
                'rating': Decimal('4.8'),
                'total_sales': 156,
                'active_properties': 24,
                'specialties': ['Hashamatli uylar', 'Shahar markazi mulklari', 'Investitsiya mulklari'],
                'team_members': [
                    {'name': 'John Smith', 'role': 'Katta agent', 'experience': 15, 'sales': 89},
                    {'name': 'Sarah Johnson', 'role': 'Mulk menejeri', 'experience': 12, 'sales': 67}
                ]
            },
            {
                'name': 'BuildRight Construction',
                'company_type': 'construction',
                'description': 'Zamonaviy turar-joy qurilishiga ixtisoslashgan yetakchi qurilish kompaniyasi.',
                'address': '456 Construction St, Biznes hududi, Toshkent',
                'phone': '+998 90 987 65 43',
                'email': 'info@buildright.uz',
                'website': 'https://buildright.uz',
                'license_number': 'CON-2024-005678',
                'founded_year': 2010,
                'rating': Decimal('4.9'),
                'total_sales': 89,
                'active_properties': 12,
                'specialties': ['Yangi qurilish', 'Zamonaviy dizayn', 'Ekologik toza'],
                'team_members': [
                    {'name': 'Mike Wilson', 'role': 'Loyiha menejeri', 'experience': 18, 'sales': 45},
                    {'name': 'Lisa Chen', 'role': 'Arxitektor', 'experience': 10, 'sales': 32}
                ]
            },
            {
                'name': 'Family First Realty',
                'company_type': 'realtor',
                'description': 'Oilalarga xavfsiz va do\'stona mahallaarda mukammal uy topishda yordam berishga bag\'ishlangan.',
                'address': '789 Family Lane, Oilaviy hudud, Toshkent',
                'phone': '+998 90 456 78 90',
                'email': 'hello@familyfirst.uz',
                'website': 'https://familyfirst.uz',
                'license_number': 'RE-2024-009876',
                'founded_year': 2008,
                'rating': Decimal('4.6'),
                'total_sales': 203,
                'active_properties': 18,
                'specialties': ['Oilaviy uylar', 'Maktab hududlari', 'Shahar chetki mulklari'],
                'team_members': [
                    {'name': 'David Kim', 'role': 'Oila maslahatchisi', 'experience': 14, 'sales': 78},
                    {'name': 'Maria Garcia', 'role': 'Hudud mutaxassisi', 'experience': 8, 'sales': 56}
                ]
            },
            {
                'name': 'Premium Properties',
                'company_type': 'realtor',
                'description': 'Yuqori darajadagi mulklar va tanqidchi mijozlar uchun eksklyuziv vakillik.',
                'address': '321 Luxury Blvd, Premium hudud, Toshkent',
                'phone': '+998 90 321 09 87',
                'email': 'luxury@premiumprops.uz',
                'website': 'https://premiumprops.uz',
                'license_number': 'RE-2024-001122',
                'founded_year': 2015,
                'rating': Decimal('4.9'),
                'total_sales': 78,
                'active_properties': 8,
                'specialties': ['Hashamatli mulklar', 'Suv bo\'yidagi mulklar', 'Shaxsiy sotuvlar'],
                'team_members': [
                    {'name': 'Robert Taylor', 'role': 'Hashamatli mulk maslahatchisi', 'experience': 20, 'sales': 45},
                    {'name': 'Jennifer White', 'role': 'VIP mijozlar menejeri', 'experience': 12, 'sales': 33}
                ]
            }
        ]
        
        for company_data in companies_data:
            if not Company.objects.filter(name=company_data['name']).exists():
                # Get a random admin user for this company
                admin_users = User.objects.filter(user_type__in=['admin', 'agent', 'seller'])
                
                company = Company.objects.create(
                    name=company_data['name'],
                    company_type=company_data['company_type'],
                    description=company_data['description'],
                    address=company_data['address'],
                    phone=company_data['phone'],
                    email=company_data['email'],
                    website=company_data['website'],
                    license_number=company_data['license_number'],
                    founded_year=company_data['founded_year'],
                    rating=company_data['rating'],
                    total_sales=company_data['total_sales'],
                    active_properties=company_data['active_properties'],
                    is_verified=True
                )
                
                # Add specialties
                for specialty_name in company_data['specialties']:
                    CompanySpecialty.objects.create(
                        company=company,
                        name=specialty_name
                    )
                
                # Add team members
                for member_data in company_data['team_members']:
                    CompanyTeamMember.objects.create(
                        company=company,
                        name=member_data['name'],
                        role=member_data['role'],
                        experience_years=member_data['experience'],
                        sales_count=member_data['sales']
                    )
                
                # Assign company to admin users
                if admin_users.exists():
                    admin_user = admin_users.first()
                    admin_user.company = company
                    admin_user.save()
                
                self.stdout.write(f'Created company: {company.name}')

    def create_properties(self):
        self.stdout.write('Creating properties...')
        
        companies = Company.objects.all()
        admin_users = User.objects.filter(user_type__in=['admin', 'agent', 'seller'])
        
        properties_data = [
            {
                'title': 'Zamonaviy shahar markazi kvartirasi',
                'description': 'Bu ajoyib zamonaviy kvartira ochiq kontseptsiya dizayni bilan jihozlangan bo\'lib, poldan shiftgacha oynalar shahar manzarasini taqdim etadi. Gurme oshxona zanglamaydigan po\'lat jihozlar va granit peshtaxta bilan jihozlangan.',
                'property_type': 'apartment',
                'price': Decimal('450000'),
                'address': '123 Shahar markazi ko\'chasi, Shahar markazi',
                'city': 'Toshkent',
                'neighborhood': 'Shahar markazi',
                'bedrooms': 2,
                'bathrooms': 2,
                'area': Decimal('120'),
                'year_built': 2020,
                'parking_spaces': 1,
                'has_garage': False,
                'has_garden': False,
                'has_pool': False,
                'has_360_tour': True,
                'featured': True,
                'amenities': ['Gym', 'Hovuz', 'Konsyerj', 'Tom bog\'i']
            },
            {
                'title': 'Hovuzli hashamatli villa',
                'description': 'Hashamatli villa keng yashash maydonlari, shaxsiy hovuz va chiroyli bog\' bilan. Zamonaviy dizayn va yuqori sifatli materiallar bilan qurilgan.',
                'property_type': 'villa',
                'price': Decimal('850000'),
                'address': '456 Tepalik ko\'chasi, Premium hudud',
                'city': 'Toshkent',
                'neighborhood': 'Tepalik',
                'bedrooms': 4,
                'bathrooms': 3,
                'area': Decimal('280'),
                'year_built': 2018,
                'parking_spaces': 3,
                'has_garage': True,
                'has_garden': True,
                'has_pool': True,
                'has_360_tour': False,
                'featured': True,
                'amenities': ['Shaxsiy hovuz', 'Bog\'', 'Vino yerto\'lasi', 'Uy kinoteatri']
            },
            {
                'title': 'Qulay oilaviy uy',
                'description': 'Xavfsiz mahallada joylashgan ajoyib oilaviy uy. Yaqin atrofda maktablar va bog\'lar mavjud. Oilalar uchun ideal.',
                'property_type': 'house',
                'price': Decimal('320000'),
                'address': '789 Oila ko\'chasi, Shahar chetki',
                'city': 'Toshkent',
                'neighborhood': 'Oilaviy mahalla',
                'bedrooms': 3,
                'bathrooms': 2,
                'area': Decimal('180'),
                'year_built': 2015,
                'parking_spaces': 2,
                'has_garage': True,
                'has_garden': True,
                'has_pool': False,
                'has_360_tour': True,
                'featured': True,
                'amenities': ['Bog\'', 'O\'yin maydoni', 'Garaj', 'Keng oshxona']
            },
            {
                'title': 'Yangi qurilgan kondominiyum',
                'description': 'Eng so\'nggi qulayliklar bilan jihozlangan yangi qurilgan kondominiyum. Zamonaviy dizayn va energiya tejamkor texnologiyalar.',
                'property_type': 'condo',
                'price': Decimal('380000'),
                'address': '321 Yangi qurilish ko\'chasi, O\'rta shahar',
                'city': 'Toshkent',
                'neighborhood': 'Yangi qurilish',
                'bedrooms': 2,
                'bathrooms': 2,
                'area': Decimal('110'),
                'year_built': 2023,
                'parking_spaces': 1,
                'has_garage': False,
                'has_garden': False,
                'has_pool': True,
                'has_360_tour': False,
                'featured': True,
                'amenities': ['Fitnes zal', 'Umumiy hovuz', 'Xavfsizlik', 'Lift']
            },
            {
                'title': 'Penthouse Suite',
                'description': 'Hashamatli penthouse ajoyib shahar manzarasi bilan. Yuqori darajadagi tugatish va eksklyuziv qulayliklar.',
                'property_type': 'apartment',
                'price': Decimal('1200000'),
                'address': '555 Baland minora, Shahar markazi',
                'city': 'Toshkent',
                'neighborhood': 'Hashamatli minora',
                'bedrooms': 3,
                'bathrooms': 3,
                'area': Decimal('220'),
                'year_built': 2021,
                'parking_spaces': 2,
                'has_garage': True,
                'has_garden': False,
                'has_pool': True,
                'has_360_tour': True,
                'featured': True,
                'amenities': ['Tom terras', 'Shaxsiy lift', 'Konsyerj', 'Vino yerto\'lasi']
            },
            {
                'title': 'Shahar chetidagi rancho uyi',
                'description': 'Tinch mahallada joylashgan keng rancho uyi. Katta hovli va tabiiy muhit.',
                'property_type': 'house',
                'price': Decimal('275000'),
                'address': '888 G\'arb ko\'chasi, Tinch mahalla',
                'city': 'Toshkent',
                'neighborhood': 'G\'arbiy tomon',
                'bedrooms': 3,
                'bathrooms': 2,
                'area': Decimal('160'),
                'year_built': 2012,
                'parking_spaces': 2,
                'has_garage': True,
                'has_garden': True,
                'has_pool': False,
                'has_360_tour': False,
                'featured': False,
                'amenities': ['Katta hovli', 'Garaj', 'Kamin', 'Oshxona orolchasi']
            }
        ]
        
        # Add more properties with random data
        additional_properties = []
        property_types = ['apartment', 'house', 'condo', 'villa']
        neighborhoods = ['Chilonzor', 'Yunusobod', 'Mirzo Ulug\'bek', 'Shayxontohur', 'Yakkasaroy']
        
        for i in range(20):  # Create 20 additional properties
            prop_type = random.choice(property_types)
            neighborhood = random.choice(neighborhoods)
            
            additional_properties.append({
                'title': f'{prop_type.title()} {neighborhood}da #{i+1}',
                'description': f'Ajoyib {prop_type} {neighborhood} mahallasida. Zamonaviy qulayliklar va yaxshi joylashuv.',
                'property_type': prop_type,
                'price': Decimal(str(random.randint(200000, 900000))),
                'address': f'{random.randint(100, 999)} {neighborhood} ko\'chasi',
                'city': 'Toshkent',
                'neighborhood': neighborhood,
                'bedrooms': random.randint(1, 5),
                'bathrooms': random.randint(1, 4),
                'area': Decimal(str(random.randint(80, 300))),
                'year_built': random.randint(2000, 2023),
                'parking_spaces': random.randint(0, 3),
                'has_garage': random.choice([True, False]),
                'has_garden': random.choice([True, False]),
                'has_pool': random.choice([True, False]),
                'has_360_tour': random.choice([True, False]),
                'featured': random.choice([True, False]),
                'amenities': random.sample(['Gym', 'Hovuz', 'Xavfsizlik', 'Lift', 'Bog\'', 'Garaj'], k=random.randint(2, 4))
            })
        
        all_properties = properties_data + additional_properties
        
        for prop_data in all_properties:
            if not Property.objects.filter(title=prop_data['title']).exists():
                # Get random company and owner
                company = random.choice(companies) if companies.exists() else None
                owner = random.choice(admin_users) if admin_users.exists() else None
                
                property_obj = Property.objects.create(
                    title=prop_data['title'],
                    description=prop_data['description'],
                    property_type=prop_data['property_type'],
                    price=prop_data['price'],
                    address=prop_data['address'],
                    city=prop_data['city'],
                    neighborhood=prop_data['neighborhood'],
                    bedrooms=prop_data['bedrooms'],
                    bathrooms=prop_data['bathrooms'],
                    area=prop_data['area'],
                    year_built=prop_data['year_built'],
                    parking_spaces=prop_data['parking_spaces'],
                    has_garage=prop_data['has_garage'],
                    has_garden=prop_data['has_garden'],
                    has_pool=prop_data['has_pool'],
                    has_360_tour=prop_data['has_360_tour'],
                    status='active',
                    views_count=random.randint(50, 500),
                    inquiries_count=random.randint(5, 50),
                    rating=Decimal(str(round(random.uniform(4.0, 5.0), 1))),
                    owner=owner,
                    company=company,
                    featured=prop_data['featured']
                )
                
                # Add amenities
                for amenity_name in prop_data['amenities']:
                    PropertyAmenity.objects.create(
                        property=property_obj,
                        name=amenity_name
                    )
                
                self.stdout.write(f'Created property: {property_obj.title}')

    def create_news(self):
        self.stdout.write('Creating news articles...')
        
        companies = Company.objects.all()
        admin_users = User.objects.filter(user_type__in=['admin', 'agent', 'seller'])
        
        news_data = [
            {
                'title': 'Bahor sotuvi - Barcha mulklarga 20% chegirma',
                'slug': 'bahor-sotuvi-chegirma',
                'content': 'Premium mulklarga sezilarli chegirmalar bilan bahor aksiyamizdan foydalaning. Bu cheklangan vaqt taklifi barcha turdagi mulklar uchun amal qiladi.',
                'excerpt': 'Premium mulklarga sezilarli chegirmalar bilan bahor aksiyamizdan foydalaning.',
                'status': 'published',
                'views_count': 1250
            },
            {
                'title': 'Yangi hashamatli loyiha ochilishi',
                'slug': 'yangi-hashamatli-loyiha',
                'content': 'Eng zamonaviy qulayliklar va zamonaviy dizayn bilan jihozlangan eng so\'nggi hashamatli loyihamizni taqdim etamiz. Bu loyiha Toshkent shahrining eng yaxshi hududida joylashgan.',
                'excerpt': 'Eng zamonaviy qulayliklar bilan jihozlangan eng so\'nggi hashamatli loyihamizni taqdim etamiz.',
                'status': 'published',
                'views_count': 890
            },
            {
                'title': 'Bozor tendentsiyalari hisoboti 2024-yil 1-chorak',
                'slug': 'bozor-tendentsiyalari-2024',
                'content': 'Hozirgi ko\'chmas mulk bozori tendentsiyalari va prognozlarining keng qamrovli tahlili. Narxlar o\'sishi va yangi imkoniyatlar haqida.',
                'excerpt': 'Hozirgi ko\'chmas mulk bozori tendentsiyalari va prognozlarining keng qamrovli tahlili.',
                'status': 'published',
                'views_count': 650
            },
            {
                'title': 'Investitsiya uchun eng yaxshi hududlar',
                'slug': 'investitsiya-hududlari',
                'content': 'Ko\'chmas mulkka investitsiya qilish uchun Toshkent shahrining eng istiqbolli hududlari haqida batafsil ma\'lumot.',
                'excerpt': 'Ko\'chmas mulkka investitsiya qilish uchun eng istiqbolli hududlar.',
                'status': 'published',
                'views_count': 420
            },
            {
                'title': 'Yangi qurilish texnologiyalari',
                'slug': 'yangi-qurilish-texnologiyalari',
                'content': 'Zamonaviy qurilish sohasidagi eng so\'nggi texnologiyalar va ularning ko\'chmas mulk bozoriga ta\'siri.',
                'excerpt': 'Zamonaviy qurilish sohasidagi eng so\'nggi texnologiyalar.',
                'status': 'draft',
                'views_count': 0
            }
        ]
        
        for news_item in news_data:
            if not NewsArticle.objects.filter(slug=news_item['slug']).exists():
                # Get random company and author
                company = random.choice(companies) if companies.exists() else None
                author = random.choice(admin_users) if admin_users.exists() else None
                
                published_at = None
                if news_item['status'] == 'published':
                    published_at = timezone.now() - timedelta(days=random.randint(1, 30))
                
                article = NewsArticle.objects.create(
                    title=news_item['title'],
                    slug=news_item['slug'],
                    content=news_item['content'],
                    excerpt=news_item['excerpt'],
                    author=author,
                    company=company,
                    status=news_item['status'],
                    views_count=news_item['views_count'],
                    published_at=published_at
                )
                
                self.stdout.write(f'Created news article: {article.title}')
