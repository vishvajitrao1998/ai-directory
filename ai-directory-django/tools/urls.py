from django.urls import path
from . import views

# app_name = 'tools'

urlpatterns = [
    
    # Important Pages
    path('', views.home, name='home'),
    path('submit-tool', views.tool_submission, name='tool_submission'),
    path('remove-tool', views.remove_tool, name='remove_tool'),
    path('update-tool', views.update_tool, name='update_tool'),
    path('advertise', views.advertisement, name='advertisement'),

    # API Endpoints
    path('api/tools/', views.get_tools, name='get_tools'),
    path('api/tools/<str:tool_id>/', views.get_tool, name='get_tool'),
    path('api/categories/', views.get_categories, name='get_categories'),
    path('api/stats/', views.get_stats, name='get_stats'),
    path('api/submit/', views.submit_tool, name='submit_tool'),
    path('api/remove/', views.request_removal, name='request_removal'),
    path('api/contact/', views.contact_us, name='contact_us'),
    path("api/currencies/", views.get_currency_list, name="get_currency_list"),
    path("api/listing/prices", views.get_prices_by_currency, name="get_prices_by_currency"),
    path("api/advertise/prices", views.get_prices_by_currency_advertise, name="get_prices_by_currency_advertise"),

    # Close
    
    # Admin endpoints
    path('admin/submissions/', views.get_submissions, name='get_submissions'),
    path('admin/submissions/<int:submission_id>/approve/', views.approve_submission, name='approve_submission'),
    path('admin/removal-requests/', views.get_removal_requests, name='get_removal_requests'),
    path('admin/init-sample-data/', views.init_sample_data, name='init_sample_data'),

    # Company Pages
    path('p/privacy-policy', views.privacy_policy, name='privacy-policy'),
    path('p/contact', views.contact, name='contact_us'),
    path('p/about', views.privacy_policy, name='privacy-policy'),
    path('p/terms-condition', views.privacy_policy, name='privacy-policy'),
    path('how-obtain-ai-works', views.working, name='working'),
]

