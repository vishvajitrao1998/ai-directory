from django.db import models
from django.utils import timezone
import json


class AITool(models.Model):
    PRICING_CHOICES = [
        ('free', 'Free'),
        ('paid', 'Paid'),
        ('freemium', 'Freemium'),
        ('open_source', 'Open Source'),
    ]
    
    LISTING_TYPE_CHOICES = [
        ('simple', 'Simple'),
        ('verified', 'Verified'),
        ('featured', 'Featured'),
    ]
    
    name = models.CharField(max_length=200)
    description = models.TextField()
    detailed_description = models.TextField(blank=True, null=True)
    category = models.CharField(max_length=100)
    pricing = models.CharField(max_length=50, choices=PRICING_CHOICES, default='free')
    website_url = models.URLField(max_length=500)
    logo_url = models.URLField(max_length=500, blank=True, null=True)
    listing_type = models.CharField(max_length=50, choices=LISTING_TYPE_CHOICES, default='simple')
    tags = models.TextField(blank=True, null=True)  # JSON string of tags array
    features = models.TextField(blank=True, null=True)  # JSON string of features array
    date_added = models.DateTimeField(default=timezone.now)
    rating = models.FloatField(default=0.0)
    is_active = models.BooleanField(default=True)
    
    # Contact information
    contact_name = models.CharField(max_length=200, blank=True, null=True)
    contact_email = models.EmailField(max_length=200, blank=True, null=True)
    contact_company = models.CharField(max_length=200, blank=True, null=True)
    
    # Verification status
    is_verified = models.BooleanField(default=False)
    verification_date = models.DateTimeField(blank=True, null=True)
    
    class Meta:
        db_table = 'ai_tools'
        ordering = ['name']
    
    def __str__(self):
        return self.name
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'detailed_description': self.detailed_description,
            'category': self.category,
            'pricing': self.pricing,
            'website_url': self.website_url,
            'logo_url': self.logo_url,
            'listing_type': self.listing_type,
            'tags': json.loads(self.tags) if self.tags else [],
            'features': json.loads(self.features) if self.features else [],
            'date_added': self.date_added.isoformat() if self.date_added else None,
            'rating': self.rating,
            'is_active': self.is_active,
            'contact_name': self.contact_name,
            'contact_email': self.contact_email,
            'contact_company': self.contact_company,
            'is_verified': self.is_verified,
            'verification_date': self.verification_date.isoformat() if self.verification_date else None
        }
    
    def get_tags_list(self):
        """Return tags as a list"""
        return json.loads(self.tags) if self.tags else []
    
    def set_tags_list(self, tags_list):
        """Set tags from a list"""
        self.tags = json.dumps(tags_list) if tags_list else None
    
    def get_features_list(self):
        """Return features as a list"""
        return json.loads(self.features) if self.features else []
    
    def set_features_list(self, features_list):
        """Set features from a list"""
        self.features = json.dumps(features_list) if features_list else None


class ToolSubmission(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]
    
    PRICING_CHOICES = [
        ('free', 'Free'),
        ('paid', 'Paid'),
        ('freemium', 'Freemium'),
        ('open_source', 'Open Source'),
    ]
    
    LISTING_TYPE_CHOICES = [
        ('simple', 'Simple'),
        ('verified', 'Verified'),
        ('featured', 'Featured'),
    ]
    
    tool_name = models.CharField(max_length=200)
    tool_website = models.URLField(max_length=500)
    tool_category = models.CharField(max_length=100)
    tool_pricing = models.CharField(max_length=50, choices=PRICING_CHOICES)
    tool_description = models.TextField()
    tool_detailed_description = models.TextField(blank=True, null=True)
    tool_features = models.TextField(blank=True, null=True)  # JSON string
    tool_tags = models.TextField(blank=True, null=True)  # JSON string
    listing_type = models.CharField(max_length=50, choices=LISTING_TYPE_CHOICES, default='simple')
    
    # Contact information
    contact_name = models.CharField(max_length=200)
    contact_email = models.EmailField(max_length=200)
    contact_company = models.CharField(max_length=200, blank=True, null=True)
    
    # Submission metadata
    submission_date = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='pending')
    admin_notes = models.TextField(blank=True, null=True)
    
    class Meta:
        db_table = 'tool_submissions'
        ordering = ['-submission_date']
    
    def __str__(self):
        return f"Submission: {self.tool_name}"
    
    def to_dict(self):
        return {
            'id': self.id,
            'tool_name': self.tool_name,
            'tool_website': self.tool_website,
            'tool_category': self.tool_category,
            'tool_pricing': self.tool_pricing,
            'tool_description': self.tool_description,
            'tool_detailed_description': self.tool_detailed_description,
            'tool_features': json.loads(self.tool_features) if self.tool_features else [],
            'tool_tags': json.loads(self.tool_tags) if self.tool_tags else [],
            'listing_type': self.listing_type,
            'contact_name': self.contact_name,
            'contact_email': self.contact_email,
            'contact_company': self.contact_company,
            'submission_date': self.submission_date.isoformat() if self.submission_date else None,
            'status': self.status,
            'admin_notes': self.admin_notes
        }


class ToolRemovalRequest(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('verified', 'Verified'),
        ('completed', 'Completed'),
        ('rejected', 'Rejected'),
    ]
    
    VERIFICATION_METHOD_CHOICES = [
        ('email', 'Email Verification'),
        ('domain', 'Domain Verification'),
        ('documentation', 'Documentation'),
        ('other', 'Other'),
    ]
    
    REMOVAL_REASON_CHOICES = [
        ('discontinued', 'Tool Discontinued'),
        ('rebranding', 'Rebranding'),
        ('privacy', 'Privacy Concerns'),
        ('inaccurate', 'Inaccurate Information'),
        ('other', 'Other'),
    ]
    
    tool_name = models.CharField(max_length=200)
    tool_website = models.URLField(max_length=500)
    tool_id = models.CharField(max_length=100, blank=True, null=True)  # Optional tool ID
    
    # Owner information
    owner_name = models.CharField(max_length=200)
    owner_email = models.EmailField(max_length=200)
    owner_company = models.CharField(max_length=200, blank=True, null=True)
    
    # Verification and reason
    verification_method = models.CharField(max_length=100, choices=VERIFICATION_METHOD_CHOICES)
    removal_reason = models.CharField(max_length=100, choices=REMOVAL_REASON_CHOICES)
    additional_details = models.TextField(blank=True, null=True)
    
    # Request metadata
    request_date = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='pending')
    admin_notes = models.TextField(blank=True, null=True)
    
    class Meta:
        db_table = 'tool_removal_requests'
        ordering = ['-request_date']
    
    def __str__(self):
        return f"Removal Request: {self.tool_name}"
    
    def to_dict(self):
        return {
            'id': self.id,
            'tool_name': self.tool_name,
            'tool_website': self.tool_website,
            'tool_id': self.tool_id,
            'owner_name': self.owner_name,
            'owner_email': self.owner_email,
            'owner_company': self.owner_company,
            'verification_method': self.verification_method,
            'removal_reason': self.removal_reason,
            'additional_details': self.additional_details,
            'request_date': self.request_date.isoformat() if self.request_date else None,
            'status': self.status,
            'admin_notes': self.admin_notes
        }

