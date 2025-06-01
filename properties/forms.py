from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Submit, Row, Column
from .models import Property, PropertyInquiry

class PropertySearchForm(forms.Form):
    PROPERTY_TYPES = [
        ('', 'Barcha turlar'),
        ('apartment', 'Kvartira'),
        ('house', 'Uy'),
        ('condo', 'Kondominiyum'),
        ('villa', 'Villa'),
    ]
    
    BEDROOM_CHOICES = [
        ('', 'Xonalar soni'),
        (1, '1 xona'),
        (2, '2 xona'),
        (3, '3 xona'),
        (4, '4 xona'),
        (5, '5+ xona'),
    ]
    
    SORT_CHOICES = [
        ('', 'Saralash'),
        ('price_low', 'Narx: Pastdan yuqoriga'),
        ('price_high', 'Narx: Yuqoridan pastga'),
        ('newest', 'Eng yangilari'),
        ('rating', 'Eng yuqori baholangan'),
    ]
    
    search_query = forms.CharField(
        max_length=255,
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': 'Joylashuv, mulk turi bo\'yicha qidiring...',
            'class': 'form-control'
        })
    )
    
    price_min = forms.DecimalField(
        required=False,
        widget=forms.NumberInput(attrs={
            'placeholder': 'Min narx',
            'class': 'form-control'
        })
    )
    
    price_max = forms.DecimalField(
        required=False,
        widget=forms.NumberInput(attrs={
            'placeholder': 'Max narx',
            'class': 'form-control'
        })
    )
    
    property_type = forms.ChoiceField(
        choices=PROPERTY_TYPES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    
    bedrooms = forms.ChoiceField(
        choices=BEDROOM_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    
    sort_by = forms.ChoiceField(
        choices=SORT_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'})
    )

class PropertyInquiryForm(forms.ModelForm):
    class Meta:
        model = PropertyInquiry
        fields = ['name', 'email', 'phone', 'message']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ismingizni kiriting'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'email@example.com'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '+998 90 123 45 67'
            }),
            'message': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Bu mulk haqida savolingizni yozing...'
            }),
        }

class PropertyForm(forms.ModelForm):
    class Meta:
        model = Property
        fields = [
            'title', 'description', 'property_type', 'price', 'address',
            'city', 'neighborhood', 'bedrooms', 'bathrooms', 'area',
            'year_built', 'parking_spaces', 'has_garage', 'has_garden',
            'has_pool', 'has_360_tour', 'status', 'featured'
        ]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'property_type': forms.Select(attrs={'class': 'form-select'}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'address': forms.TextInput(attrs={'class': 'form-control'}),
            'city': forms.TextInput(attrs={'class': 'form-control'}),
            'neighborhood': forms.TextInput(attrs={'class': 'form-control'}),
            'bedrooms': forms.NumberInput(attrs={'class': 'form-control'}),
            'bathrooms': forms.NumberInput(attrs={'class': 'form-control'}),
            'area': forms.NumberInput(attrs={'class': 'form-control'}),
            'year_built': forms.NumberInput(attrs={'class': 'form-control'}),
            'parking_spaces': forms.NumberInput(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('title', css_class='form-group col-md-6 mb-0'),
                Column('property_type', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            'description',
            Row(
                Column('price', css_class='form-group col-md-4 mb-0'),
                Column('city', css_class='form-group col-md-4 mb-0'),
                Column('neighborhood', css_class='form-group col-md-4 mb-0'),
                css_class='form-row'
            ),
            'address',
            Row(
                Column('bedrooms', css_class='form-group col-md-3 mb-0'),
                Column('bathrooms', css_class='form-group col-md-3 mb-0'),
                Column('area', css_class='form-group col-md-3 mb-0'),
                Column('year_built', css_class='form-group col-md-3 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('parking_spaces', css_class='form-group col-md-6 mb-0'),
                Column('status', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('has_garage', css_class='form-group col-md-3 mb-0'),
                Column('has_garden', css_class='form-group col-md-3 mb-0'),
                Column('has_pool', css_class='form-group col-md-3 mb-0'),
                Column('has_360_tour', css_class='form-group col-md-3 mb-0'),
                css_class='form-row'
            ),
            'featured',
            Submit('submit', 'Saqlash', css_class='btn btn-success')
        )
