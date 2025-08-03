from django.contrib import admin
from .models import *
from .utility import send_mail

@admin.register(AITool)
class AIToolAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'pricing', 'listing_type', 'rating', 'is_active', 'date_added']
    list_filter = ['category', 'pricing', 'listing_type', 'is_active', 'is_verified']
    search_fields = ['name', 'description', 'website_url']
    list_editable = ['is_active', 'rating', 'listing_type']
    ordering = ['-date_added']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'description', 'detailed_description', 'category', 'pricing', 'website_url', 'logo_url')
        }),
        ('Listing Details', {
            'fields': ('listing_type', 'rating', 'is_active', 'tags', 'features')
        }),
        ('Contact Information', {
            'fields': ('contact_name', 'contact_email', 'contact_company', 'user_timezone')
        }),
        ('Verification', {
            'fields': ('is_verified', 'verification_date')
        }),
    )
    
    # def save_model(self, request, obj, form, change):
    #     # Auto-verify featured and verified listings
    #     if obj.listing_type in ['verified', 'featured']:
    #         obj.is_verified = True
    #         if not obj.verification_date:
    #             from django.utils import timezone
    #             obj.verification_date = timezone.now()
    #     super().save_model(request, obj, form, change)


@admin.action(description="Approve Selected Tools")   
def approve_submissions(self, request, queryset):
    """Approve selected submissions and create AI tools"""
    approved_count = queryset.filter(status='pending').update(status='approved')
    # approved_count = 0
    # for submission in queryset.filter(status='pending'):
    #     # Create AI tool from submission
    #     tool = AITool.objects.create(
    #         name=submission.tool_name,
    #         description=submission.tool_description,
    #         extra_links=submission.extra_links,
    #         category=submission.tool_category,
    #         pricing=submission.tool_pricing,
    #         website_url=submission.tool_website,
    #         listing_type=submission.listing_type,
    #         tags=submission.tool_tags,
    #         features=submission.tool_features,
    #         contact_name=submission.contact_name,
    #         contact_email=submission.contact_email,
    #         contact_company=submission.contact_company,
    #         is_verified=submission.listing_type in ['verified', 'featured']
    #     )
        
    #     if tool.is_verified:
    #         from django.utils import timezone
    #         tool.verification_date = timezone.now()
    #         tool.save()
        
    #     # Update submission status
    #     submission.status = 'approved'
    #     submission.admin_notes = f'Approved and created as tool ID: {tool.id}'
    #     submission.save()
    #     approved_count += 1
    self.message_user(request, f'Successfully approved {approved_count} submissions.')

@admin.action(description="Reject Selected Tools")   
def reject_submissions(self, request, queryset):
        """Reject selected submissions"""
        rejected_count = queryset.filter(status='pending').update(status='rejected')
        self.message_user(request, f'Successfully rejected {rejected_count} submissions.')

@admin.action(description="Ready For Live")   
def ready_for_live(self, request, queryset):
        """Mark tool to ready live"""
        qs = queryset.filter(status='approved')
        for tool in qs:
            print(tool.contact_email)
            # Code to send an email to every one along with payment link
            sendMail = send_mail(tool.contact_email, tool.tool_ref_num, tool.contact_name, 'for_payment')
        queryset.filter(status='approved').update(status='ready_to_live')
        self.message_user(request, f'Selected tools are marked as ready to live and payment email is sent also.')
 

@admin.register(ToolSubmission)
class ToolSubmissionAdmin(admin.ModelAdmin):
    list_display = ['tool_name', 'tool_category', 'tool_pricing', 'listing_type', 'contact_name', 'status', 'submission_date']
    list_filter = ['status', 'tool_category', 'tool_pricing', 'listing_type', 'submission_date']
    search_fields = ['tool_name', 'tool_website', 'contact_name', 'contact_email']
    list_editable = ['status']
    ordering = ['-submission_date']
    readonly_fields = ['tool_name','tool_ref_num', 'tool_category', 'tool_pricing', 'listing_type', 'contact_name', 'submission_date', 'tool_website', 'contact_email', 'contact_company','tool_description', 'extra_links','tool_features', 'tool_tags']
    fieldsets = (
        ('Tool Information', {
            'fields': ('tool_ref_num', 'tool_name', 'tool_website', 'tool_category', 'tool_pricing', 'tool_description', 'extra_links')
        }),
        ('Additional Details', {
            'fields': ('tool_features', 'tool_tags', 'listing_type')
        }),
        ('Contact Information', {
            'fields': ('contact_name', 'contact_email', 'contact_company', 'user_timezone')
        }),
        ('Submission Status', {
            'fields': ('status', 'admin_notes', 'submission_date')
        }),
    )

    actions = [approve_submissions, reject_submissions, ready_for_live]

    def get_actions(self, request):
        actions = super().get_actions(request)
        if request.user.is_superuser:
            # Keep only these actions
            allowed = ['approve_submissions', 'reject_submissions', 'ready_for_live']
            actions = {name: action for name, action in actions.items() if name in allowed}

        elif request.user.is_staff:
            # Only allow this one
            allowed = ['ready_for_live']
            actions = {name: action for name, action in actions.items() if name in allowed}

        return actions

@admin.register(ToolRemovalRequest)
class ToolRemovalRequestAdmin(admin.ModelAdmin):
    list_display = ['tool_name', 'tool_website', 'owner_name', 'removal_reason', 'status', 'request_date']
    list_filter = ['status', 'removal_reason', 'verification_method', 'request_date']
    search_fields = ['tool_name', 'tool_website', 'owner_name', 'owner_email']
    list_editable = ['status']
    ordering = ['-request_date']
    readonly_fields = ['request_date']
    
    fieldsets = (
        ('Tool Information', {
            'fields': ('tool_name', 'tool_website', 'tool_id')
        }),
        ('Owner Information', {
            'fields': ('owner_name', 'owner_email', 'owner_company')
        }),
        ('Removal Details', {
            'fields': ('verification_method', 'removal_reason', 'additional_details')
        }),
        ('Request Status', {
            'fields': ('status', 'admin_notes', 'request_date')
        }),
    )
    
    actions = ['mark_as_verified', 'mark_as_completed']
    
    def mark_as_verified(self, request, queryset):
        """Mark removal requests as verified"""
        updated = queryset.update(status='verified')
        self.message_user(request, f'Successfully marked {updated} requests as verified.')
    
    mark_as_verified.short_description = "Mark as verified"
    
    def mark_as_completed(self, request, queryset):
        """Mark removal requests as completed"""
        updated = queryset.update(status='completed')
        self.message_user(request, f'Successfully marked {updated} requests as completed.')
    
    mark_as_completed.short_description = "Mark as completed"


@admin.register(ContactUs)
class ContactUsAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'country']
    list_filter = ['name', 'email', 'country']
    search_fields = ['name', 'email', 'country']
    # list_editable = ['name']
    ordering = ['-contact_date']
    readonly_fields = ['contact_date']
    
    fieldsets = (
        ('Person Information', {
            'fields': ('name', 'email', 'country' ,'desc')
        }),
        
    )


@admin.register(Currency)
class CurrencyAdmin(admin.ModelAdmin):
    list_display = ['currency_name', 'currency_code']
    list_filter = ['currency_name', 'currency_code']
    search_fields = ['currency_name', 'currency_code']
    ordering = ['-created_date']
    readonly_fields = ['created_date']
    fieldsets = (
        ('Currency Information', {
            'fields': ('currency_name', 'currency_code', 'flag', 'symbol', 'is_active', 'created_date')
        }),
        
    )

@admin.register(ListingPlan)
class ListingPlanAdmin(admin.ModelAdmin):
    list_display = ['plan_name', 'is_active']
    list_filter = ['plan_name', 'is_active']
    search_fields = ['plan_name', 'is_active']
    ordering = ['-created_date']
    readonly_fields = ['created_date']
    # fieldsets = (
    #     ('Currency Information', {
    #         'fields': ('currency_name', 'currency_code', 'flag')
    #     }),
        
    # )

@admin.register(ListingPlanPrice)
class ListingPlanPriceAdmin(admin.ModelAdmin):
    list_display = ['get_plan_name', 'get_plan_currency', 'price', 'discount_price', 'is_active']
    list_filter = ['price', 'discount_price', 'is_active']
    search_fields = ['price', 'discount_price', 'is_active']
    ordering = ['-created_date']
    readonly_fields = ['created_date']
    # fieldsets = (
    #     ('Currency Information', {
    #         'fields': ('currency_name', 'currency_code', 'flag')
    #     }),
        
    # )

    def get_plan_name(self, obj):
        return obj.pricing_plan.plan_name
    
    def get_plan_currency(self, obj):
        return obj.currency.currency_name
    
    get_plan_name.short_description = 'Plan Name'
    get_plan_currency.short_description = 'Plan Currency'

@admin.register(AdvertisementPlan)
class AdvertisementPlanAdmin(admin.ModelAdmin):
    list_display = ['plan_name', 'plan_duration', 'is_active']
    list_filter = ['plan_name', 'plan_duration', 'is_active']
    search_fields = ['plan_name', 'plan_duration', 'is_active']
    ordering = ['-created_date']
    readonly_fields = ['created_date']

    


@admin.register(AdvertisementPlanPrice)
class AdvertisementPlanPriceAdmin(admin.ModelAdmin):
    list_display = ['get_plan_name', 'get_plan_currency', 'price', 'get_plan_duration', 'is_active']
    list_filter = ['price', 'discount_price', 'is_active']
    search_fields = ['price', 'discount_price', 'is_active']
    ordering = ['-created_date']
    readonly_fields = ['created_date']

    def get_plan_name(self, obj):
        return obj.pricing_plan.plan_name
    
    def get_plan_currency(self, obj):
        return obj.currency.currency_name
    
    def get_plan_duration(self, obj):
        return obj.pricing_plan.plan_duration
    
    
    get_plan_name.short_description = 'Plan Name'
    get_plan_currency.short_description = 'Plan Currency'
    get_plan_duration.short_description = 'Plan Duration'


# Customize admin site headers
admin.site.site_header = "Obtain.AI Admin"
admin.site.site_title = "Obtain.AI Admin Portal"
admin.site.index_title = "Welcome to Obtain.AI Administration"