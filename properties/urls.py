from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('properties/', views.properties_list, name='properties_list'),
    path('property/<int:pk>/', views.property_detail, name='property_detail'),
    path('compare/', views.compare_properties, name='compare_properties'),
    path('add-to-comparison/', views.add_to_comparison, name='add_to_comparison'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    
    # Admin URLs
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin/properties/', views.admin_properties, name='admin_properties'),
    path('admin/properties/add/', views.admin_add_property, name='admin_add_property'),
    path('admin/properties/<int:pk>/edit/', views.admin_edit_property, name='admin_edit_property'),
]
