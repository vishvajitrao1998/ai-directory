from django.urls import path
from . import views
from . import auth_views
from . import dashboard_views

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
    # API endpoints for AJAX requests
    path('api/check-username/', auth_views.check_username_availability, name='check_username'),
    path('api/check-email/', auth_views.check_email_availability, name='check_email'),
    path('api/signup/', auth_views.signup_view, name='account_creation'),

    # API endpoints
    path('api/tool-stats/', dashboard_views.get_tool_stats, name='api_tool_stats'),
    path('api/toggle-tool/<int:tool_id>/', dashboard_views.toggle_tool_status, name='api_toggle_tool'),

    # Authentication URLs
    path('login/', auth_views.login_view, name='login'),
    path('signup/', auth_views.signup_view, name='signup'),
    path('logout/', auth_views.logout_view, name='logout'),
    path('forgot-password/', auth_views.forgot_password_view, name='forgot_password'),
    path('reset-password/<uidb64>/<token>/', auth_views.reset_password_view, name='reset_password'),

    path('dashboard', dashboard_views.dashboard_home, name='dashboard'),
    
    # Tools management
    path('dashboard/tools/', dashboard_views.tools_list, name='tools_list'),
    path('dashboard/tools/submit/', dashboard_views.submit_tool, name='submit_tool'),
    path('dashboard/tools/update/<int:tool_id>/', dashboard_views.update_tool, name='update_tool'),
    path('dashboard/tools/delete/<int:tool_id>/', dashboard_views.delete_tool, name='delete_tool'),
    
    # Advertisement
    path('dashboard/advertise/', dashboard_views.advertise_tool, name='advertise_tool'),
    
    # Plans and Analytics
    path('dashboard/plans/', dashboard_views.plans, name='plans'),
    path('dashboard/analytics/', dashboard_views.analytics, name='analytics'),
    
    # User settings
    path('dashboard/profile/', dashboard_views.profile_settings, name='profile_settings'),
    path('dashboard/account/', dashboard_views.account_settings, name='account_settings'),
    path('dashboard/help/', dashboard_views.help_center, name='help_center'),
    path('dashboard/pricing/', dashboard_views.pricing, name='pricing'),
    path('dashboard/logout/', dashboard_views.user_logout, name='logout'),
    # Close

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

