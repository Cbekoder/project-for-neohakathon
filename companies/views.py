from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Company

def companies_list(request):
    companies = Company.objects.filter(is_verified=True)
    
    search_query = request.GET.get('search')
    company_type = request.GET.get('type')
    
    if search_query:
        companies = companies.filter(
            Q(name__icontains=search_query) |
            Q(description__icontains=search_query)
        )
    
    if company_type:
        companies = companies.filter(company_type=company_type)
    
    paginator = Paginator(companies, 8)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'companies': page_obj.object_list,
        'search_query': search_query,
        'selected_type': company_type,
    }
    return render(request, 'companies/list.html', context)

def company_detail(request, pk):
    company = get_object_or_404(Company, pk=pk, is_verified=True)
    properties = company.properties.filter(status='active')[:6]
    news_articles = company.news_articles.filter(status='published')[:3]
    
    context = {
        'company': company,
        'properties': properties,
        'news_articles': news_articles,
    }
    return render(request, 'companies/detail.html', context)
