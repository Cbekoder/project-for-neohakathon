from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from .models import UserProfile

User = get_user_model()

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    user_type = forms.ChoiceField(choices=User.USER_TYPES, initial='buyer')
    
    class Meta:
        model = User
        fields = ("username", "email", "user_type", "password1", "password2")
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        user.user_type = self.cleaned_data["user_type"]
        if commit:
            user.save()
        return user

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['bio', 'location', 'website', 'budget_min', 'budget_max', 'preferred_locations']
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
            'website': forms.URLInput(attrs={'class': 'form-control'}),
            'budget_min': forms.NumberInput(attrs={'class': 'form-control'}),
            'budget_max': forms.NumberInput(attrs={'class': 'form-control'}),
            'preferred_locations': forms.Textarea(attrs={'rows': 2, 'class': 'form-control'}),
        }
