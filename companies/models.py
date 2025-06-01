from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Company(models.Model):
    COMPANY_TYPES = (
        ('realtor', 'Rieltor'),
        ('construction', 'Qurilish'),
        ('development', 'Rivojlantirish'),
    )
    
    name = models.CharField(max_length=255)
    company_type = models.CharField(max_length=20, choices=COMPANY_TYPES)
    description = models.TextField()
    logo = models.ImageField(upload_to='company_logos/', blank=True, null=True)
    cover_image = models.ImageField(upload_to='company_covers/', blank=True, null=True)
    address = models.TextField()
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    website = models.URLField(blank=True)
    license_number = models.CharField(max_length=50)
    founded_year = models.IntegerField()
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.0)
    total_sales = models.IntegerField(default=0)
    active_properties = models.IntegerField(default=0)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = "Companies"

class CompanySpecialty(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='specialties')
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return f"{self.company.name} - {self.name}"

class CompanyTeamMember(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='team_members')
    name = models.CharField(max_length=255)
    role = models.CharField(max_length=100)
    experience_years = models.IntegerField()
    sales_count = models.IntegerField(default=0)
    photo = models.ImageField(upload_to='team_photos/', blank=True, null=True)
    
    def __str__(self):
        return f"{self.name} - {self.company.name}"
