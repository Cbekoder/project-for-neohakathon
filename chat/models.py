from django.db import models
from django.contrib.auth import get_user_model
from properties.models import Property

User = get_user_model()

class ChatRoom(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='chat_rooms')
    buyer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='buyer_chats')
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name='seller_chats')
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.buyer.username} - {self.property.title}"
    
    class Meta:
        unique_together = ['property', 'buyer', 'seller']

class ChatMessage(models.Model):
    MESSAGE_TYPES = (
        ('text', 'Matn'),
        ('system', 'Tizim'),
        ('image', 'Rasm'),
        ('file', 'Fayl'),
    )
    
    room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    message_type = models.CharField(max_length=10, choices=MESSAGE_TYPES, default='text')
    content = models.TextField()
    file = models.FileField(upload_to='chat_files/', blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.sender.username}: {self.content[:50]}"
    
    class Meta:
        ordering = ['timestamp']

class Appointment(models.Model):
    APPOINTMENT_TYPES = (
        ('viewing', 'Ko\'rish'),
        ('meeting', 'Uchrashuv'),
        ('consultation', 'Maslahat'),
        ('contract_signing', 'Shartnoma imzolash'),
    )
    
    STATUS_CHOICES = (
        ('scheduled', 'Rejalashtirilgan'),
        ('confirmed', 'Tasdiqlangan'),
        ('completed', 'Tugallangan'),
        ('cancelled', 'Bekor qilingan'),
    )
    
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    buyer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='buyer_appointments')
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name='seller_appointments')
    appointment_type = models.CharField(max_length=20, choices=APPOINTMENT_TYPES)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    date = models.DateField()
    time = models.TimeField()
    duration = models.DurationField()
    location = models.CharField(max_length=255)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='scheduled')
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.title} - {self.date} {self.time}"
