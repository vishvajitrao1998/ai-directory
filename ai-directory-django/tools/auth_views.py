from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
import json

def login_view(request):
    """User login view"""
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        remember_me = request.POST.get('remember_me')
        
        # Try to authenticate with username or email
        user = authenticate(request, username=username, password=password)
        
        if user is None:
            # Try to find user by email if username authentication failed
            try:
                user_obj = User.objects.get(email=username)
                user = authenticate(request, username=user_obj.username, password=password)
            except User.DoesNotExist:
                user = None
        
        if user is not None:
            if user.is_active:
                login(request, user)
                
                # Set session expiry based on remember me
                if not remember_me:
                    request.session.set_expiry(0)  # Session expires when browser closes
                else:
                    request.session.set_expiry(30 * 24 * 60 * 60)  # 30 days
                
                messages.success(request, f'Welcome back, {user.first_name or user.username}!')
                
                # Redirect to next page or dashboard
                next_page = request.GET.get('next', 'dashboard')
                return redirect(next_page)
            else:
                messages.error(request, 'Your account has been deactivated. Please contact support.')
        else:
            messages.error(request, 'Invalid username/email or password. Please try again.')
    
    return render(request, 'auth/login.html')

def signup_view(request):
    """User registration view"""
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        print('Done')
        first_name = request.POST.get('first_name', '').strip()
        
        last_name = request.POST.get('last_name', '').strip()
        username = request.POST.get('username', '').strip()
        email = request.POST.get('email', '').strip()
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        terms = request.POST.get('terms')
        # newsletter = request.POST.get('newsletter')


        print(first_name, last_name, email, password1, password2, terms)
        
        # Validation
        errors = []
        
        if not first_name:
            errors.append('First name is required.')
        
        if not last_name:
            errors.append('Last name is required.')
        
        if not username:
            errors.append('Username is required.')
        elif len(username) < 3:
            errors.append('Username must be at least 3 characters long.')
        elif User.objects.filter(username=username).exists():
            errors.append('Username already exists. Please choose a different one.')
        
        if not email:
            errors.append('Email address is required.')
        elif User.objects.filter(email=email).exists():
            errors.append('Email address already registered. Please use a different email or sign in.')
        
        if not password1:
            errors.append('Password is required.')
        elif len(password1) < 8:
            errors.append('Password must be at least 8 characters long.')
        
        if password1 != password2:
            errors.append('Passwords do not match.')
        
        if not terms:
            errors.append('You must agree to the Terms of Service and Privacy Policy.')
        
        if errors:
            for error in errors:
                messages.error(request, error)
        else:
            try:
                # Create user
                user = User.objects.create_user(
                    username=username,
                    email=email,
                    password=password1,
                    first_name=first_name,
                    last_name=last_name
                )
                
                # Create user profile if you have one
                # UserProfile.objects.create(
                #     user=user,
                #     newsletter_subscription=bool(newsletter)
                # )
                
                # Send welcome email (optional)
                if hasattr(settings, 'EMAIL_HOST'):
                    try:
                        send_welcome_email(user)
                    except Exception as e:
                        print(f"Failed to send welcome email: {e}")
                
                # messages.success(request, 'Account created successfully! You can now sign in.')
                return JsonResponse({
                        'success': True,
                        'message': 'Account is created'
                    })
                
            except Exception as e:
                messages.error(request, 'An error occurred while creating your account. Please try again.')
                print(f"Signup error: {e}")
    
    return render(request, 'auth/signup.html')

def logout_view(request):
    """User logout view"""
    if request.user.is_authenticated:
        username = request.user.first_name or request.user.username
        logout(request)
        messages.success(request, f'Goodbye, {username}! You have been logged out successfully.')
    
    return redirect('auth:login')

def forgot_password_view(request):
    """Forgot password view"""
    if request.method == 'POST':
        email = request.POST.get('email', '').strip()
        
        if not email:
            messages.error(request, 'Please enter your email address.')
        else:
            try:
                user = User.objects.get(email=email)
                
                # Generate password reset token
                token = default_token_generator.make_token(user)
                uid = urlsafe_base64_encode(force_bytes(user.pk))
                
                # Send password reset email
                current_site = get_current_site(request)
                reset_link = f"http://{current_site.domain}/auth/reset-password/{uid}/{token}/"
                
                subject = 'Password Reset - AI Directory'
                message = f"""
                Hi {user.first_name or user.username},
                
                You requested a password reset for your AI Directory account.
                
                Click the link below to reset your password:
                {reset_link}
                
                If you didn't request this, please ignore this email.
                
                Best regards,
                AI Directory Team
                """
                
                if hasattr(settings, 'EMAIL_HOST'):
                    try:
                        send_mail(
                            subject,
                            message,
                            settings.DEFAULT_FROM_EMAIL,
                            [email],
                            fail_silently=False,
                        )
                        messages.success(request, 'Password reset link has been sent to your email.')
                    except Exception as e:
                        messages.error(request, 'Failed to send email. Please try again later.')
                        print(f"Email sending error: {e}")
                else:
                    # For development without email setup
                    messages.success(request, f'Password reset link: {reset_link}')
                
            except User.DoesNotExist:
                # Don't reveal if email exists or not for security
                messages.success(request, 'If an account with that email exists, a password reset link has been sent.')
    
    return render(request, 'auth/forgot_password.html')

def reset_password_view(request, uidb64, token):
    """Password reset confirmation view"""
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    
    if user is not None and default_token_generator.check_token(user, token):
        if request.method == 'POST':
            password1 = request.POST.get('password1')
            password2 = request.POST.get('password2')
            
            if not password1:
                messages.error(request, 'Password is required.')
            elif len(password1) < 8:
                messages.error(request, 'Password must be at least 8 characters long.')
            elif password1 != password2:
                messages.error(request, 'Passwords do not match.')
            else:
                user.set_password(password1)
                user.save()
                messages.success(request, 'Your password has been reset successfully. You can now sign in.')
                return redirect('auth:login')
        
        return render(request, 'auth/reset_password.html', {'validlink': True})
    else:
        messages.error(request, 'The password reset link is invalid or has expired.')
        return redirect('auth:forgot_password')

# API Views for AJAX requests


@require_http_methods(["POST"])
@csrf_exempt
def check_username_availability(request):
    """Check if username is available"""
    try:
        data = json.loads(request.body)
        username = data.get('username', '').strip()
        
        if len(username) < 3:
            return JsonResponse({
                'available': False,
                'message': 'Username must be at least 3 characters long'
            })
        
        if User.objects.filter(username=username).exists():
            return JsonResponse({
                'available': False,
                'message': 'Username is already taken'
            })
        
        return JsonResponse({
            'available': True,
            'message': 'Username is available'
        })
        
    except Exception as e:
        return JsonResponse({
            'available': False,
            'message': 'Error checking username availability'
        })

@require_http_methods(["POST"])
@csrf_exempt
def check_email_availability(request):
    """Check if email is available"""
    try:
        data = json.loads(request.body)
        email = data.get('email', '').strip()
        
        if User.objects.filter(email=email).exists():
            return JsonResponse({
                'available': False,
                'message': 'Email is already registered'
            })
        
        return JsonResponse({
            'available': True,
            'message': 'Email is available'
        })
        
    except Exception as e:
        return JsonResponse({
            'available': False,
            'message': 'Error checking email availability'
        })

# Helper functions

def send_welcome_email(user):
    """Send welcome email to new user"""
    subject = 'Welcome to AI Directory!'
    message = f"""
    Hi {user.first_name or user.username},
    
    Welcome to AI Directory! We're excited to have you join our community.
    
    You can now:
    - Submit your AI tools for review
    - Discover amazing AI tools from other creators
    - Track your tool's performance with analytics
    - Advertise your tools to reach more users
    
    Get started by visiting your dashboard and submitting your first AI tool.
    
    If you have any questions, don't hesitate to contact our support team.
    
    Best regards,
    AI Directory Team
    """
    
    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [user.email],
        fail_silently=False,
    )

