from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Count, Q
from django.core.paginator import Paginator
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
import json
from .models import AITool

# Assuming you have these models - adjust imports as needed
# from .models import AITool, Advertisement, Plan, Analytics

@login_required
def dashboard_home(request):
    """Main dashboard homepage showing user statistics"""
    user = request.user
    
    # Get user's tools statistics
    total_tools = AITool.objects.filter(user=user).count()
    active_tools = AITool.objects.filter(user=user, is_active=True).count()
    pending_tools = AITool.objects.filter(user=user, is_active=True).count()
    approved_tools = AITool.objects.filter(user=user, is_active=True).count()
    
    # Tools for advertisement (assuming there's an advertisement field)
    tools_for_advertisement = AITool.objects.filter(user=user, is_active=True).count()
    
    # Recent tools
    recent_tools = AITool.objects.filter(user=user).order_by('-created_date')[:5]
    
    context = {
        'total_tools': total_tools,
        'active_tools': active_tools,
        'pending_tools': pending_tools,
        'approved_tools': approved_tools,
        'tools_for_advertisement': tools_for_advertisement,
        'recent_tools': recent_tools,
    }
    
    return render(request, 'dashboard/home.html', context)

@login_required
def tools_list(request):
    """Display all user's tools with pagination"""
    user = request.user
    tools = AITool.objects.filter(user=user, is_active=True).order_by('-created_date')
    
    # Pagination
    paginator = Paginator(tools, 10)  # Show 10 tools per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'tools': page_obj,
    }
    
    return render(request, 'dashboard/tools_list.html', context)

@login_required
def submit_tool(request):
    """Submit a new tool for admin review"""
    if request.method == 'POST':
        # Handle tool submission form
        name = request.POST.get('name')
        description = request.POST.get('description')
        category = request.POST.get('category')
        url = request.POST.get('url')
        
        tool = AITool.objects.create(
            user=request.user,
            name=name,
            description=description,
            category=category,
            url=url,
            status='pending'
        )
        
        messages.success(request, 'Tool submitted successfully for admin review!')
        return redirect('dashboard:tools_list')
    
    return render(request, 'dashboard/submit_tool.html')

@login_required
def update_tool(request, tool_id):
    """Update an existing tool"""
    tool = get_object_or_404(AITool, id=tool_id, user=request.user)
    
    if request.method == 'POST':
        tool.name = request.POST.get('name')
        tool.description = request.POST.get('description')
        tool.category = request.POST.get('category')
        tool.url = request.POST.get('url')
        tool.save()
        
        messages.success(request, 'Tool updated successfully!')
        return redirect('dashboard:tools_list')
    
    context = {'tool': tool}
    return render(request, 'dashboard/update_tool.html', context)

@login_required
@require_POST
def delete_tool(request, tool_id):
    """Delete a tool"""
    tool = get_object_or_404(AITool, id=tool_id, user=request.user)
    tool.delete()
    messages.success(request, 'Tool deleted successfully!')
    return redirect('dashboard:tools_list')

@login_required
def advertise_tool(request):
    """Request to advertise AI tools"""
    user_tools = AITool.objects.filter(user=request.user, is_active= True)
    
    if request.method == 'POST':
        tool_id = request.POST.get('tool_id')
        advertisement_type = request.POST.get('advertisement_type')
        duration = request.POST.get('duration')
        
        tool = get_object_or_404(AITool, id=tool_id, user=request.user)
        
        # Create advertisement request (assuming you have an Advertisement model)
        # Advertisement.objects.create(
        #     user=request.user,
        #     tool=tool,
        #     advertisement_type=advertisement_type,
        #     duration=duration,
        #     status='pending'
        # )
        
        messages.success(request, 'Advertisement request submitted successfully!')
        return redirect('dashboard:advertise_tool')
    
    context = {'user_tools': user_tools}
    return render(request, 'dashboard/advertise_tool.html', context)

@login_required
def plans(request):
    """Display available plans"""
    # plans = Plan.objects.filter(is_active=True)
    # user_plan = request.user.current_plan if hasattr(request.user, 'current_plan') else None
    
    context = {
        # 'plans': plans,
        # 'user_plan': user_plan,
    }
    return render(request, 'dashboard/plans.html', context)

@login_required
def analytics(request):
    """Display tool analytics"""
    user = request.user
    tools = AITool.objects.filter(user=user)
    
    # Sample analytics data - replace with actual analytics logic
    analytics_data = []
    for tool in tools:
        analytics_data.append({
            'tool': tool,
            'views': 0,  # Replace with actual view count
            'clicks': 0,  # Replace with actual click count
            'conversions': 0,  # Replace with actual conversion count
        })
    
    context = {
        'analytics_data': analytics_data,
        'tools': tools,
    }
    return render(request, 'dashboard/analytics.html', context)

@login_required
def profile_settings(request):
    """User profile settings"""
    if request.method == 'POST':
        user = request.user
        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')
        user.email = request.POST.get('email')
        user.save()
        
        messages.success(request, 'Profile updated successfully!')
        return redirect('dashboard:profile_settings')
    
    return render(request, 'dashboard/profile_settings.html')

@login_required
def account_settings(request):
    """Account settings"""
    return render(request, 'dashboard/account_settings.html')

@login_required
def help_center(request):
    """Help center"""
    return render(request, 'dashboard/help_center.html')

@login_required
def pricing(request):
    """Pricing page"""
    return render(request, 'dashboard/pricing.html')

def user_logout(request):
    """Logout user"""
    logout(request)
    messages.success(request, 'You have been logged out successfully!')
    return redirect('login')  # Adjust redirect as needed

# API endpoints for AJAX requests
@login_required
def get_tool_stats(request):
    """API endpoint to get tool statistics"""
    user = request.user
    stats = {
        'total_tools': AITool.objects.filter(user=user).count(),
        'active_tools': AITool.objects.filter(user=user, is_active=True).count(),
        'pending_tools': AITool.objects.filter(user=user, status='pending').count(),
        'approved_tools': AITool.objects.filter(user=user, status='approved').count(),
    }
    return JsonResponse(stats)

@login_required
@csrf_exempt
def toggle_tool_status(request, tool_id):
    """Toggle tool active status"""
    if request.method == 'POST':
        tool = get_object_or_404(AITool, id=tool_id, user=request.user)
        tool.is_active = not tool.is_active
        tool.save()
        
        return JsonResponse({
            'success': True,
            'is_active': tool.is_active,
            'message': f'Tool {"activated" if tool.is_active else "deactivated"} successfully!'
        })
    
    return JsonResponse({'success': False, 'message': 'Invalid request method'})

