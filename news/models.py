from django.db import models
from django.contrib.auth import get_user_model
from companies.models import Company

User = get_user_model()

class NewsArticle(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Qoralama'),
        ('published', 'Nashr qilingan'),
        ('archived', 'Arxivlangan'),
    )
    
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    content = models.TextField()
    excerpt = models.TextField(blank=True)
    featured_image = models.ImageField(upload_to='news_images/', blank=True, null=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='news_articles')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    views_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    published_at = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return self.title
    
    def increment_views(self):
        self.views_count += 1
        self.save(update_fields=['views_count'])
    
    class Meta:
        ordering = ['-created_at']
