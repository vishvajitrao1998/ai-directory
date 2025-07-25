from django.contrib import admin
from .models import AITool, ToolSubmission, ToolRemovalRequest


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
            'fields': ('contact_name', 'contact_email', 'contact_company')
        }),
        ('Verification', {
            'fields': ('is_verified', 'verification_date')
        }),
    )
    
    def save_model(self, request, obj, form, change):
        # Auto-verify featured and verified listings
        if obj.listing_type in ['verified', 'featured']:
            obj.is_verified = True
            if not obj.verification_date:
                from django.utils import timezone
                obj.verification_date = timezone.now()
        super().save_model(request, obj, form, change)


@admin.action(description="Approve Selected Tools")   
def approve_submissions(self, request, queryset):
    """Approve selected submissions and create AI tools"""
    approved_count = 0
    print("This is calling")
    for submission in queryset.filter(status='pending'):
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
            from django.utils import timezone
            tool.verification_date = timezone.now()
            tool.save()
        
        # Update submission status
        submission.status = 'approved'
        submission.admin_notes = f'Approved and created as tool ID: {tool.id}'
        submission.save()
        approved_count += 1
    
    self.message_user(request, f'Successfully approved {approved_count} submissions.')

@admin.action(description="Reject Selected Tools")   
def reject_submissions(self, request, queryset):
        """Reject selected submissions"""
        rejected_count = queryset.filter(status='pending').update(status='rejected')
        self.message_user(request, f'Successfully rejected {rejected_count} submissions.')


@admin.register(ToolSubmission)
class ToolSubmissionAdmin(admin.ModelAdmin):
    list_display = ['tool_name', 'tool_category', 'tool_pricing', 'listing_type', 'contact_name', 'status', 'submission_date']
    list_filter = ['status', 'tool_category', 'tool_pricing', 'listing_type', 'submission_date']
    search_fields = ['tool_name', 'tool_website', 'contact_name', 'contact_email']
    list_editable = ['status']
    ordering = ['-submission_date']
    readonly_fields = ['submission_date']
    
    fieldsets = (
        ('Tool Information', {
            'fields': ('tool_name', 'tool_website', 'tool_category', 'tool_pricing', 'tool_description', 'tool_detailed_description')
        }),
        ('Additional Details', {
            'fields': ('tool_features', 'tool_tags', 'listing_type')
        }),
        ('Contact Information', {
            'fields': ('contact_name', 'contact_email', 'contact_company')
        }),
        ('Submission Status', {
            'fields': ('status', 'admin_notes', 'submission_date')
        }),
    )
    actions = [approve_submissions, reject_submissions]
 
    

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


# Customize admin site headers
admin.site.site_header = "AI Directory Admin"
admin.site.site_title = "AI Directory Admin Portal"
admin.site.index_title = "Welcome to AI Directory Administration"