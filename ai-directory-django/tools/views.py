from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.core.paginator import Paginator
from django.db.models import Q, Count
from django.utils import timezone
from django.shortcuts import get_object_or_404, render
import json
from .models import *
from .utility import *


@require_http_methods(["GET"])
def get_currency_list(request):
    currencies = Currency.objects.all()
    data = [c.to_dict() for c in currencies]
    return JsonResponse({"currencies": data})

@require_http_methods(["GET"])
def get_prices_by_currency(request):
    currency = request.GET.get("currency")
    data = []
    if not currency:
        return JsonResponse({"error": "currency parameter is required"}, status=400)

    prices = ListingPlanPrice.objects.filter(currency=currency, is_active=True).values('currency__currency_code', 'currency__symbol', 'price', 'pricing_plan__plan_name')
    for d in prices:
        data.append (
            {
                'code': d.get('currency__currency_code'),
                'plan_name': d.get('pricing_plan__plan_name'),
                'symbol': d.get('currency__symbol'),
                'price': int(d.get('price')),
                'formated_price': f"{d.get('currency__symbol')}{int(d.get('price'))}"
            }
        )
    return JsonResponse({"prices": data})



@require_http_methods(["GET"])
def get_prices_by_currency_advertise(request):
    currency = request.GET.get("currency")
    data = []
    if not currency:
        return JsonResponse({"error": "currency parameter is required"}, status=400)

    prices = AdvertisementPlanPrice.objects.filter(currency=currency, is_active=True).values('currency__currency_code', 'currency__symbol', 'price', 'pricing_plan__plan_name', 'pricing_plan__plan_duration')
    for d in prices:
        data.append (
            {
                'code': d.get('currency__currency_code'),
                'plan_name': d.get('pricing_plan__plan_name'),
                'plan_duration': d.get('pricing_plan__plan_duration'),
                'symbol': d.get('currency__symbol'),
                'price': int(d.get('price')),
                'formated_price': f"{d.get('currency__symbol')}{int(d.get('price'))}"
            }
        )
    print(data)
    return JsonResponse({"prices": data})





@require_http_methods(["GET"])
def get_tools(request):
    """Get all AI tools with filtering and pagination"""
    try:
        # Get query parameters
        page = int(request.GET.get('page', 1))
        per_page = int(request.GET.get('per_page', 20))
        category = request.GET.get('category', '')
        pricing = request.GET.get('pricing', '')
        listing_type = request.GET.get('listing_type', '')
        search = request.GET.get('search', '')
        sort_by = request.GET.get('sort_by', 'name')
        
        # Build query
        queryset = AITool.objects.filter(is_active=True)
        
        # Apply filters
        if category:
            queryset = queryset.filter(category=category)
        if pricing:
            queryset = queryset.filter(pricing=pricing)
        if listing_type:
            queryset = queryset.filter(listing_type=listing_type)
        if search:
            queryset = queryset.filter(
                Q(name__icontains=search) |
                Q(description__icontains=search) |
                Q(tags__icontains=search)
            )
        
        # Apply sorting
        if sort_by == 'name':
            queryset = queryset.order_by('name')
        elif sort_by == 'date':
            queryset = queryset.order_by('-date_added')
        elif sort_by == 'rating':
            queryset = queryset.order_by('-rating')
        elif sort_by == 'category':
            queryset = queryset.order_by('category')
        
        # Paginate
        paginator = Paginator(queryset, per_page)
        page_obj = paginator.get_page(page)
        
        tools = [tool.to_dict() for tool in page_obj]
        
        return JsonResponse({
            'success': True,
            'tools': tools,
            'pagination': {
                'page': page,
                'per_page': per_page,
                'total': paginator.count,
                'pages': paginator.num_pages,
                'has_next': page_obj.has_next(),
                'has_prev': page_obj.has_previous()
            }
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)
    

@require_http_methods(["GET"])
def get_tool(request, tool_id):
    """Get single AI tool by ID"""
    try:
        print(tool_id)
        tool = get_object_or_404(AITool, id=tool_id, is_active=True)
        return JsonResponse({
            'success': True,
            'tool': tool.to_dict()
        })
        
    except Exception as e:
        print(e)
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)


@require_http_methods(["GET"])
def get_categories(request):
    """Get tool categories"""
    try:
        categories = AITool.objects.filter(is_active=True).values_list('category', flat=True).distinct()
        category_list = list(categories)
        
        return JsonResponse({
            'success': True,
            'categories': category_list
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)


@require_http_methods(["GET"])
def get_stats(request):
    """Get tool statistics"""
    try:
        total_tools = AITool.objects.filter(is_active=True).count()
        total_categories = AITool.objects.filter(is_active=True).values('category').distinct().count()
        free_tools = AITool.objects.filter(
            is_active=True,
            pricing__in=['free', 'open_source']
        ).count()
        
        return JsonResponse({
            'success': True,
            'stats': {
                'total_tools': total_tools,
                'total_categories': total_categories,
                'free_tools': free_tools
            }
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)


@csrf_exempt
@require_http_methods(["POST"])
def submit_tool(request):
    """Submit new tool"""
    try:
        data = json.loads(request.body)
        tool_ref_num = generate_application_reference()
        
        # Validate required fields
        required_fields = [
            'toolName', 'toolWebsite', 'toolCategory', 'toolPricing',
            'toolDescription', 'contactName', 'contactEmail'
        ]
        
        for field in required_fields:
            if not data.get(field):
                return JsonResponse({
                    'success': False,
                    'error': f'Missing required field: {field}'
                }, status=400)
        
        # Process features and tags
        features = []
        if data.get('toolFeatures'):
            features = [f.strip() for f in data['toolFeatures'].split('\n') if f.strip()]
        
        tags = []
        if data.get('toolTags'):
            tags = [t.strip() for t in data['toolTags'].split(',') if t.strip()]

        extra_links = []
        if data.get('ExtraLink1'):
            extra_links.append(data.get('ExtraLink1'))
        if data.get('ExtraLink2'):
            extra_links.append(data.get('ExtraLink2'))
        if data.get('ExtraLink3'):
            extra_links.append(data.get('ExtraLink3'))

        extraLinks = ','.join(extra_links)

        # Create submission record
        submission = ToolSubmission.objects.create(
            tool_name=data['toolName'],
            tool_ref_num=tool_ref_num,
            tool_website=data['toolWebsite'],
            user_timezone = data['user_timezone'],
            extra_links=extraLinks,
            tool_category=data['toolCategory'],
            tool_pricing=data['toolPricing'],
            tool_description=data['toolDescription'],
            tool_features=json.dumps(features) if features else None,
            tool_tags=json.dumps(tags) if tags else None,
            listing_type=data.get('listingType', 'simple'),
            contact_name=data['contactName'],
            contact_email=data['contactEmail'],
            contact_company=data.get('contactCompany', '')
        )

        # Code to send email to the user and admin to notify a new tool is requested
        sendMail = send_mail(data['contactEmail'], tool_ref_num, data['contactName'], 'for_tool_creation')
        return JsonResponse({
            'success': True,
            'message': 'Tool submission received successfully',
            'submission_id': submission.id,
            'tool_ref_num': tool_ref_num
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)


@csrf_exempt
@require_http_methods(["POST"])
def request_removal(request):
    """Request tool removal"""
    try:
        data = json.loads(request.body)
        
        # Validate required fields
        required_fields = [
            'toolNameRemove', 'toolWebsiteRemove', 'ownerName',
            'ownerEmail', 'verificationMethod', 'removalReason'
        ]
        
        for field in required_fields:
            if not data.get(field):
                return JsonResponse({
                    'success': False,
                    'error': f'Missing required field: {field}'
                }, status=400)
        
        # Create removal request
        removal_request = ToolRemovalRequest.objects.create(
            tool_name=data['toolNameRemove'],
            tool_website=data['toolWebsiteRemove'],
            tool_id=data.get('toolIdRemove', ''),
            owner_name=data['ownerName'],
            owner_email=data['ownerEmail'],
            owner_company=data.get('ownerCompany', ''),
            verification_method=data['verificationMethod'],
            removal_reason=data['removalReason'],
            additional_details=data.get('additionalDetails', '')
        )
        
        return JsonResponse({
            'success': True,
            'message': 'Tool removal request submitted successfully',
            'request_id': removal_request.id
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)


# Admin endpoints
@require_http_methods(["GET"])
def get_submissions(request):
    """Get tool submissions (admin)"""
    try:
        page = int(request.GET.get('page', 1))
        per_page = int(request.GET.get('per_page', 20))
        status = request.GET.get('status', '')
        
        queryset = ToolSubmission.objects.all()
        if status:
            queryset = queryset.filter(status=status)
        
        queryset = queryset.order_by('-submission_date')
        paginator = Paginator(queryset, per_page)
        page_obj = paginator.get_page(page)
        
        submissions = [submission.to_dict() for submission in page_obj]
        
        return JsonResponse({
            'success': True,
            'submissions': submissions,
            'pagination': {
                'page': page,
                'per_page': per_page,
                'total': paginator.count,
                'pages': paginator.num_pages
            }
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)


@csrf_exempt
@require_http_methods(["POST"])
def approve_submission(request, submission_id):
    """Approve submission (admin)"""
    try:
        submission = get_object_or_404(ToolSubmission, id=submission_id)
        
        # Create AI tool from submission
        tool = AITool.objects.create(
            name=submission.tool_name,
            description=submission.tool_description,
            detailed_description=submission.tool_detailed_description,
            category=submission.tool_category,
            pricing=submission.tool_pricing,
            website_url=submission.tool_website,
            listing_type=submission.listing_type,
            tags=submission.tool_tags,
            features=submission.tool_features,
            contact_name=submission.contact_name,
            contact_email=submission.contact_email,
            contact_company=submission.contact_company,
            is_verified=submission.listing_type in ['verified', 'featured']
        )
        
        if tool.is_verified:
            tool.verification_date = timezone.now()
            tool.save()
        
        # Update submission status
        submission.status = 'approved'
        submission.save()
        
        return JsonResponse({
            'success': True,
            'message': 'Submission approved and tool created',
            'tool_id': tool.id
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)


@require_http_methods(["GET"])
def get_removal_requests(request):
    """Get removal requests (admin)"""
    try:
        page = int(request.GET.get('page', 1))
        per_page = int(request.GET.get('per_page', 20))
        status = request.GET.get('status', '')
        
        queryset = ToolRemovalRequest.objects.all()
        if status:
            queryset = queryset.filter(status=status)
        
        queryset = queryset.order_by('-request_date')
        paginator = Paginator(queryset, per_page)
        page_obj = paginator.get_page(page)
        
        requests = [req.to_dict() for req in page_obj]
        
        return JsonResponse({
            'success': True,
            'removal_requests': requests,
            'pagination': {
                'page': page,
                'per_page': per_page,
                'total': paginator.count,
                'pages': paginator.num_pages
            }
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)


@csrf_exempt
@require_http_methods(["POST"])
def init_sample_data(request):
    """Initialize sample data (admin)"""
    try:
        # Check if data already exists
        if AITool.objects.count() > 0:
            return JsonResponse({
                'success': False,
                'error': 'Sample data already exists'
            }, status=400)
        
        # Sample tools data
        sample_tools = [
            {
                'name': 'ChatGPT',
                'description': 'Advanced AI chatbot for conversations, writing, and problem-solving',
                'detailed_description': 'ChatGPT is a state-of-the-art conversational AI developed by OpenAI. It can assist with writing, coding, analysis, creative tasks, and much more.',
                'category': 'text-generation',
                'pricing': 'freemium',
                'website_url': 'https://chat.openai.com',
                'listing_type': 'featured',
                'tags': json.dumps(['conversation', 'writing', 'coding', 'analysis']),
                'features': json.dumps(['Natural conversation', 'Code generation', 'Text analysis', 'Creative writing']),
                'rating': 4.8
            },
            {
                'name': 'Midjourney',
                'description': 'AI-powered image generation from text descriptions',
                'detailed_description': 'Midjourney is an independent research lab exploring new mediums of thought and expanding the imaginative powers of the human species.',
                'category': 'image-generation',
                'pricing': 'paid',
                'website_url': 'https://midjourney.com',
                'listing_type': 'verified',
                'tags': json.dumps(['art', 'design', 'creativity', 'images']),
                'features': json.dumps(['High-quality images', 'Artistic styles', 'Discord integration', 'Commercial use']),
                'rating': 4.7
            },
            {
                'name': 'GitHub Copilot',
                'description': 'AI pair programmer that helps you write code faster',
                'detailed_description': 'GitHub Copilot is an AI coding assistant that helps developers write code faster and with less effort.',
                'category': 'development',
                'pricing': 'paid',
                'website_url': 'https://github.com/features/copilot',
                'listing_type': 'verified',
                'tags': json.dumps(['coding', 'programming', 'development', 'productivity']),
                'features': json.dumps(['Code completion', 'Multiple languages', 'IDE integration', 'Context awareness']),
                'rating': 4.6
            }
        ]
        
        for tool_data in sample_tools:
            AITool.objects.create(**tool_data)
        
        return JsonResponse({
            'success': True,
            'message': f'Successfully created {len(sample_tools)} sample tools'
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)



@csrf_exempt
@require_http_methods(["POST"])
def contact_us(request):
    """Submit Contact"""
    try:
        data = json.loads(request.body)
        
        # Validate required fields
        required_fields = [
            'name', 'email', 'desc'
        ]
        for field in required_fields:
            if not data.get(field):
                return JsonResponse({
                    'success': False,
                    'error': f'Missing required field: {field}'
                }, status=400)
        
        # Create submission record
        submission = ContactUs.objects.create(
            name=data['name'],
            email=data['email'],
            country=data['country'],
            desc=data['desc'],
        )
    
        return JsonResponse({
            'success': True,
            'message': 'Contact saved successfully',
            'submission_id': submission.id
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)


def home(request):
    return render(request, 'index.html')

def tool_submission(request):
    return render(request, 'submit-tool.html')


def remove_tool(request):
    return render(request, 'remove-tool.html')

def update_tool(request):
    return render(request, 'update-tool.html')


def advertisement(request):
    return render(request, 'advertisement.html')


# pages
def privacy_policy(request):
    return render(request, 'privacy-policy.html')

def contact(request):
    return render(request, 'contact-form.html')


def working(request):
    return render(request, 'working.html')

