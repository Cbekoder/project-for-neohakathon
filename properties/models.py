from django.db import models
from django.contrib.auth import get_user_model
from companies.models import Company

User = get_user_model()

class Property(models.Model):
    PROPERTY_TYPES = (
        ('apartment', 'Kvartira'),
        ('house', 'Uy'),
        ('condo', 'Kondominiyum'),
        ('villa', 'Villa'),
        ('office', 'Ofis'),
        ('commercial', 'Tijorat'),
    )
    
    STATUS_CHOICES = (
        ('active', 'Faol'),
        ('pending', 'Kutilmoqda'),
        ('sold', 'Sotilgan'),
        ('rented', 'Ijaraga berilgan'),
    )
    
    title = models.CharField(max_length=255)
    description = models.TextField()
    property_type = models.CharField(max_length=20, choices=PROPERTY_TYPES)
    price = models.DecimalField(max_digits=12, decimal_places=2)
    address = models.TextField()
    city = models.CharField(max_length=100)
    neighborhood = models.CharField(max_length=100)
    bedrooms = models.IntegerField()
    bathrooms = models.IntegerField()
    area = models.DecimalField(max_digits=10, decimal_places=2)
    year_built = models.IntegerField(null=True, blank=True)
    parking_spaces = models.IntegerField(default=0)
    has_garage = models.BooleanField(default=False)
    has_garden = models.BooleanField(default=False)
    has_pool = models.BooleanField(default=False)
    has_360_tour = models.BooleanField(default=False)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    views_count = models.IntegerField(default=0)
    inquiries_count = models.IntegerField(default=0)
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.0)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='properties')
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='properties')
    featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title
    
    def increment_views(self):
        self.views_count += 1
        self.save(update_fields=['views_count'])
    
    class Meta:
        verbose_name_plural = "Properties"
        ordering = ['-created_at']

class PropertyImage(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='property_images/')
    caption = models.CharField(max_length=255, blank=True)
    is_primary = models.BooleanField(default=False)
    order = models.IntegerField(default=0)
    
    def __str__(self):
        return f"{self.property.title} - Rasm {self.order}"
    
    class Meta:
        ordering = ['order']

class PropertyAmenity(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='amenities')
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return f"{self.property.title} - {self.name}"

class PropertyComparison(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    properties = models.ManyToManyField(Property)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.username} ning solishtirish ro'yxati"

class PropertyInquiry(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='inquiries')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.name} - {self.property.title}"
