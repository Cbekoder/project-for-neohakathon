import os
import requests
from django.core.management.base import BaseCommand
from django.core.files.base import ContentFile
from django.conf import settings
from properties.models import Property, PropertyImage
from companies.models import Company

class Command(BaseCommand):
    help = 'Generate sample images for properties and companies'

    def handle(self, *args, **options):
        self.stdout.write('Generating sample images...')
        
        # Create media directories if they don't exist
        os.makedirs(os.path.join(settings.MEDIA_ROOT, 'property_images'), exist_ok=True)
        os.makedirs(os.path.join(settings.MEDIA_ROOT, 'company_logos'), exist_ok=True)
        
        # Generate property images
        self.generate_property_images()
        
        # Generate company logos
        self.generate_company_logos()
        
        self.stdout.write(
            self.style.SUCCESS('Sample images generated successfully!')
        )

    def generate_property_images(self):
        properties = Property.objects.all()
        
        for property_obj in properties:
            if not property_obj.images.exists():
                # Generate 3-5 images per property
                num_images = 4
                
                for i in range(num_images):
                    try:
                        # Use placeholder service for sample images
                        width, height = 800, 600
                        image_url = f"https://picsum.photos/{width}/{height}?random={property_obj.id}{i}"
                        
                        response = requests.get(image_url, timeout=10)
                        if response.status_code == 200:
                            image_content = ContentFile(response.content)
                            
                            PropertyImage.objects.create(
                                property=property_obj,
                                image=image_content,
                                caption=f"{property_obj.title} - Rasm {i+1}",
                                is_primary=(i == 0),
                                order=i
                            )
                            
                            self.stdout.write(f'Generated image {i+1} for {property_obj.title}')
                    
                    except Exception as e:
                        self.stdout.write(
                            self.style.WARNING(f'Failed to generate image for {property_obj.title}: {e}')
                        )

    def generate_company_logos(self):
        companies = Company.objects.all()
        
        for company in companies:
            if not company.logo:
                try:
                    # Generate a simple logo placeholder
                    width, height = 200, 200
                    logo_url = f"https://via.placeholder.com/{width}x{height}/28a745/ffffff?text={company.name[0]}"
                    
                    response = requests.get(logo_url, timeout=10)
                    if response.status_code == 200:
                        logo_content = ContentFile(response.content)
                        company.logo.save(
                            f"{company.name.lower().replace(' ', '_')}_logo.png",
                            logo_content,
                            save=True
                        )
                        
                        self.stdout.write(f'Generated logo for {company.name}')
                
                except Exception as e:
                    self.stdout.write(
                        self.style.WARNING(f'Failed to generate logo for {company.name}: {e}')
                    )
