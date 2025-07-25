from django.urls import path
from . import views

# app_name = 'tools'

urlpatterns = [
    # Public API endpoints
    path('', views.home, name='home'),
    path('submit-tool', views.tool_submission, name='tool_submission'),
    path('remove-tool', views.remove_tool, name='remove_tool'),
    path('tools/', views.get_tools, name='get_tools'),
    path('tools/<int:tool_id>/', views.get_tool, name='get_tool'),
    path('categories/', views.get_categories, name='get_categories'),
    path('stats/', views.get_stats, name='get_stats'),
    path('submit/', views.submit_tool, name='submit_tool'),
    path('remove/', views.request_removal, name='request_removal'),
    
    # Admin endpoints
    path('admin/submissions/', views.get_submissions, name='get_submissions'),
    path('admin/submissions/<int:submission_id>/approve/', views.approve_submission, name='approve_submission'),
    path('admin/removal-requests/', views.get_removal_requests, name='get_removal_requests'),
    path('admin/init-sample-data/', views.init_sample_data, name='init_sample_data'),
]

