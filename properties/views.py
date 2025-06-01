from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .models import Property, PropertyComparison, PropertyInquiry
from .forms import PropertySearchForm, PropertyInquiryForm, PropertyForm
from companies.models import Company
from news.models import NewsArticle

def home(request):
    featured_properties = Property.objects.filter(featured=True, status='active')[:4]
    companies = Company.objects.filter(is_verified=True)[:4]
    latest_news = NewsArticle.objects.filter(status='published')[:3]
    
    context = {
        'featured_properties': featured_properties,
        'companies': companies,
        'latest_news': latest_news,
        'total_properties': Property.objects.filter(status='active').count(),
        'total_companies': Company.objects.filter(is_verified=True).count(),
        'total_customers': 25000,  # Static for now
        'satisfaction_rate': 98,   # Static for now
    }
    return render(request, 'properties/home.html', context)

def properties_list(request):
    form = PropertySearchForm(request.GET)
    properties = Property.objects.filter(status='active')
    
    if form.is_valid():
        search_query = form.cleaned_data.get('search_query')
        price_min = form.cleaned_data.get('price_min')
        price_max = form.cleaned_data.get('price_max')
        property_type = form.cleaned_data.get('property_type')
        bedrooms = form.cleaned_data.get('bedrooms')
        sort_by = form.cleaned_data.get('sort_by')
        
        if search_query:
            properties = properties.filter(
                Q(title__icontains=search_query) |
                Q(description__icontains=search_query) |
                Q(address__icontains=search_query) |
                Q(city__icontains=search_query)
            )
        
        if price_min:
            properties = properties.filter(price__gte=price_min)
        
        if price_max:
            properties = properties.filter(price__lte=price_max)
        
        if property_type:
            properties = properties.filter(property_type=property_type)
        
        if bedrooms:
            properties = properties.filter(bedrooms=bedrooms)
        
        if sort_by == 'price_low':
            properties = properties.order_by('price')
        elif sort_by == 'price_high':
            properties = properties.order_by('-price')
        elif sort_by == 'newest':
            properties = properties.order_by('-created_at')
        elif sort_by == 'rating':
            properties = properties.order_by('-rating')
    
    paginator = Paginator(properties, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'form': form,
        'page_obj': page_obj,
        'properties': page_obj.object_list,
        'total_properties': paginator.count,
    }
    return render(request, 'properties/list.html', context)

def property_detail(request, pk):
    property_obj = get_object_or_404(Property, pk=pk)
    property_obj.increment_views()
    
    similar_properties = Property.objects.filter(
        city=property_obj.city,
        property_type=property_obj.property_type,
        status='active'
    ).exclude(pk=property_obj.pk)[:3]
    
    if request.method == 'POST':
        inquiry_form = PropertyInquiryForm(request.POST)
        if inquiry_form.is_valid():
            inquiry = inquiry_form.save(commit=False)
            inquiry.property = property_obj
            if request.user.is_authenticated:
                inquiry.user = request.user
                inquiry.name = request.user.get_full_name() or request.user.username
                inquiry.email = request.user.email
            inquiry.save()
            property_obj.inquiries_count += 1
            property_obj.save(update_fields=['inquiries_count'])
            messages.success(request, "Sizning so'rovingiz muvaffaqiyatli yuborildi!")
            return redirect('property_detail', pk=property_obj.pk)
    else:
        inquiry_form = PropertyInquiryForm()
    
    context = {
        'property': property_obj,
        'similar_properties': similar_properties,
        'inquiry_form': inquiry_form,
    }
    return render(request, 'properties/detail.html', context)

@require_POST
@login_required
def add_to_comparison(request):
    property_id = request.POST.get('property_id')
    property_obj = get_object_or_404(Property, pk=property_id)
    
    comparison, created = PropertyComparison.objects.get_or_create(user=request.user)
    
    if comparison.properties.count() >= 2 and property_obj not in comparison.properties.all():
        return JsonResponse({'error': 'Maksimal 2 ta mulkni solishtirish mumkin'}, status=400)
    
    if property_obj in comparison.properties.all():
        comparison.properties.remove(property_obj)
        action = 'removed'
    else:
        comparison.properties.add(property_obj)
        action = 'added'
    
    return JsonResponse({
        'action': action,
        'count': comparison.properties.count()
    })

@login_required
def compare_properties(request):
    comparison = PropertyComparison.objects.filter(user=request.user).first()
    properties = comparison.properties.all() if comparison else []
    
    context = {
        'properties': properties,
    }
    return render(request, 'properties/compare.html', context)

def about(request):
    return render(request, 'properties/about.html')

def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        message = request.POST.get('message')
        subject = request.POST.get('subject')
        
        # Handle contact form submission here
        messages.success(request, "Sizning xabaringiz muvaffaqiyatli yuborildi!")
        return redirect('contact')
    
    return render(request, 'properties/contact.html')

# Admin Views
@login_required
def admin_dashboard(request):
    if not request.user.user_type in ['seller', 'agent', 'admin']:
        messages.error(request, "Sizda bu sahifaga kirish huquqi yo'q.")
        return redirect('home')
    
    user_properties = Property.objects.filter(owner=request.user)
    total_properties = user_properties.count()
    active_properties = user_properties.filter(status='active').count()
    total_views = sum(prop.views_count for prop in user_properties)
    total_inquiries = sum(prop.inquiries_count for prop in user_properties)
    
    recent_inquiries = PropertyInquiry.objects.filter(
        property__owner=request.user
    ).order_by('-created_at')[:5]
    
    context = {
        'total_properties': total_properties,
        'active_properties': active_properties,
        'total_views': total_views,
        'total_inquiries': total_inquiries,
        'recent_inquiries': recent_inquiries,
        'user_properties': user_properties[:6],
    }
    return render(request, 'admin/dashboard.html', context)

@login_required
def admin_properties(request):
    if not request.user.user_type in ['seller', 'agent', 'admin']:
        messages.error(request, "Sizda bu sahifaga kirish huquqi yo'q.")
        return redirect('home')
    
    properties = Property.objects.filter(owner=request.user).order_by('-created_at')
    
    context = {
        'properties': properties,
    }
    return render(request, 'admin/properties.html', context)

@login_required
def admin_add_property(request):
    if not request.user.user_type in ['seller', 'agent', 'admin']:
        messages.error(request, "Sizda bu sahifaga kirish huquqi yo'q.")
        return redirect('home')
    
    if request.method == 'POST':
        form = PropertyForm(request.POST, request.FILES)
        if form.is_valid():
            property_obj = form.save(commit=False)
            property_obj.owner = request.user
            if hasattr(request.user, 'company') and request.user.company:
                property_obj.company = request.user.company
            property_obj.save()
            messages.success(request, "Mulk muvaffaqiyatli qo'shildi!")
            return redirect('admin_properties')
    else:
        form = PropertyForm()
    
    context = {
        'form': form,
    }
    return render(request, 'admin/add_property.html', context)

@login_required
def admin_edit_property(request, pk):
    property_obj = get_object_or_404(Property, pk=pk, owner=request.user)
    
    if request.method == 'POST':
        form = PropertyForm(request.POST, request.FILES, instance=property_obj)
        if form.is_valid():
            form.save()
            messages.success(request, "Mulk ma'lumotlari yangilandi!")
            return redirect('admin_properties')
    else:
        form = PropertyForm(instance=property_obj)
    
    context = {
        'form': form,
        'property': property_obj,
    }
    return render(request, 'admin/edit_property.html', context)
