"""
URL configuration for ai_directory project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView
from django.http import HttpResponse
from django.shortcuts import render
import os

def serve_frontend(request, path=''):
    """Serve frontend files"""
    static_dir = os.path.join(settings.BASE_DIR, 'static')
    
    if path == '' or path == 'index.html':
        # Serve index.html for root path
        index_path = os.path.join(static_dir, 'index.html')
        if os.path.exists(index_path):
            with open(index_path, 'r') as f:
                return HttpResponse(f.read(), content_type='text/html')
    
    # For other paths, try to serve the file
    file_path = os.path.join(static_dir, path)
    if os.path.exists(file_path) and os.path.isfile(file_path):
        # Determine content type
        if path.endswith('.html'):
            content_type = 'text/html'
        elif path.endswith('.css'):
            content_type = 'text/css'
        elif path.endswith('.js'):
            content_type = 'application/javascript'
        elif path.endswith('.json'):
            content_type = 'application/json'
        else:
            content_type = 'application/octet-stream'
        
        with open(file_path, 'r') as f:
            print(file_path)
            return HttpResponse(f.read(), content_type=content_type)
    
    # If file not found, serve index.html (for SPA routing)
    index_path = os.path.join(static_dir, 'index.html')
    if os.path.exists(index_path):
        with open(index_path, 'r') as f:
            return HttpResponse(f.read(), content_type='text/html')
    
    return HttpResponse("File not found", status=404)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('tools.urls')),
    # path('<path:path>', serve_frontend, name='serve_frontend'),
    path('', include('tools.urls'), name='serve_frontend_roots'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
