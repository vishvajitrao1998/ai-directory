from django.db import models
from django.utils import timezone
import json
from django.conf import settings
from django.utils import timezone


class AITool(models.Model):
    PRICING_CHOICES = [
        ('free', 'Free'),
        ('paid', 'Paid'),
        ('freemium', 'Freemium'),
        ('open_source', 'Open Source'),
    ]
    
    LISTING_TYPE_CHOICES = [
        ('simple', 'Simple Listing'),
        ('verified', 'Verified Listing'),
        ('featured', 'Featured Listing'),
        ('bais_boost', 'Basic Boost'),
        ('pro_spotlight', 'Pro Spotlight'),
        ('ultiate_pro', 'Ultimate Pro'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='your_tools'
    )
    name = models.CharField(max_length=200)
    tool_ref_num = models.CharField(max_length=200, unique=True)
    user_timezone = models.CharField(max_length=200)
    description = models.TextField()
    extra_links = models.TextField(blank=True, null=True)
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

    ad_start_date = models.DateTimeField(blank=True, null=True)

    created_date = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    
    
    class Meta:
        db_table = 'ai_tools'
        verbose_name = "Listed AI Tool"  # Singular display name
        verbose_name_plural = "Listed AI Tool" # Plural display name
        ordering = ['name']
    
    def __str__(self):
        return self.name
    
    def to_dict(self):
        return {
            "user_id": self.user.id if self.user else None,
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
        ('ready_to_live', 'Read To Live'),
        ('live', 'Live'),
    ]
    
    PRICING_CHOICES = [
        ('free', 'Free'),
        ('paid', 'Paid'),
        ('freemium', 'Freemium'),
        ('open_source', 'Open Source'),
    ]
    
    LISTING_TYPE_CHOICES = [
        ('simple', 'Simple Listing'),
        ('verified', 'Verified Listing'),
        ('featured', 'Featured Listing'),
        ('bais_boost', 'Basic Boost'),
        ('pro_spotlight', 'Pro Spotlight'),
        ('ultiate_pro', 'Ultimate Pro'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='total_submissions'
    )
    tool_name = models.CharField(max_length=200)
    tool_ref_num = models.CharField(max_length=200, unique=True)
    tool_website = models.URLField(max_length=500)
    user_timezone = models.CharField(max_length=200)
    tool_category = models.CharField(max_length=100)
    tool_pricing = models.CharField(max_length=50, choices=PRICING_CHOICES)
    tool_description = models.TextField()
    extra_links = models.TextField(blank=True, null=True)
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
    last_modified = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'tool_submissions'
        verbose_name = "Tool Submission Request"  # Singular display name
        verbose_name_plural = "Tool Submission Request" # Plural display name
        ordering = ['-submission_date']
        
    
    def __str__(self):
        return f"Submission: {self.tool_name}"
    
    def to_dict(self):
        return {
            "user_id": self.user.id if self.user else None,
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
    tool_ref_num = models.CharField(max_length=200, unique=True)
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
    last_modified = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'tool_removal_requests'
        verbose_name = "Tool Removal Request"  # Singular display name
        verbose_name_plural = "Tool Removal Request" # Plural display name
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
    

class ContactUs(models.Model):
    
    # Contact Us
    name = models.CharField(max_length=200)
    country = models.CharField(max_length=200)
    email = models.EmailField(max_length=200)
    desc = models.TextField(blank=True, null=True)
    contact_date = models.DateTimeField(default=timezone.now)
    
    
    class Meta:
        db_table = 'contact'
        verbose_name = "Contact"  # Singular display name
        verbose_name_plural = "Contact" # Plural display name
        
        ordering = ['-contact_date']
    
    def __str__(self):
        return f"Person Name: {self.name}"
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'country': self.country,
            'email': self.email,
            'desc': self.desc,
        }
    

# AI Tool Listing Plan   
class ListingPlan(models.Model):

    plan_name = models.CharField(max_length=200)
    plan_features = models.TextField()
    is_active = models.BooleanField(default=True)
    created_date = models.DateTimeField(default=timezone.now)
    last_modified = models.DateTimeField(auto_now=True)
    
    
    class Meta:
        verbose_name = "Listing Plan"  # Singular display name
        verbose_name_plural = "Listing Plan" # Plural display name
        
        ordering = ['-created_date']
    
    def __str__(self):
        return f"Plan Name: {self.plan_name}"
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.plan_name,
            'active': self.is_active,
        }
    

# Advertisement Plan   
class AdvertisementPlan(models.Model):

    plan_name = models.CharField(max_length=200)
    plan_features = models.TextField(blank=True, null=True)
    plan_duration = models.IntegerField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_date = models.DateTimeField(default=timezone.now)
    last_modified = models.DateTimeField(auto_now=True)
    
    
    class Meta:
        verbose_name = "Advertisement Plan"  # Singular display name
        verbose_name_plural = "Advertisement Plan" # Plural display name
        
        ordering = ['-created_date']
    
    def __str__(self):
        return f"Plan Name: {self.plan_name}, Plan Duration: {self.plan_duration}"
    
    def to_dict(self):
        return {
            'id': self.id,
            'plan_name': self.plan_name,
            'plan_features': self.plan_features,
            'plan_duration': self.plan_duration,
        }
    

class Currency(models.Model):
    currency_name = models.CharField(max_length=200)
    currency_code = models.CharField(max_length=200)
    symbol = models.CharField(max_length=200)
    flag = models.TextField()
    is_active = models.BooleanField(default=True)
    created_date = models.DateTimeField(default=timezone.now)
    last_modified = models.DateTimeField(auto_now=True)


    class Meta:
        db_table = 'Currency'
        verbose_name = "Currency"  # Singular display name
        verbose_name_plural = "Currency" # Plural display name
        
        ordering = ['-created_date']


    def __str__(self):
        return f"Currency Name: {self.currency_name}, Currency Code: {self.currency_code}"
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.currency_name,
            'code': self.currency_code,
            'flag': self.flag
        }
    
    
# Model for listing plan
class ListingPlanPrice(models.Model):
    pricing_plan = models.ForeignKey(ListingPlan, on_delete=models.CASCADE, related_name='listing_plan_prices')
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE, related_name='listing_currency_plan_prices')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_date = models.DateTimeField(default=timezone.now)
    last_modified = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('pricing_plan', 'currency')  # Ensures one price per plan per currency
        db_table = 'Listing Plan Price'
        verbose_name = "Listing Plan Price"  # Singular display name
        verbose_name_plural = "Listing Plan Price" # Plural display name

    def __str__(self):
        return f"{self.pricing_plan.plan_name} - {self.currency.currency_code} {self.price}"
    

    def to_dict(self):
        return {
            'id': self.id,
            'plan_name': self.pricing_plan.plan_name,
            'currency_name': self.currency.currency_name,
            'currency_code': self.currency.currency_code,
            'symbol': self.currency.symbol,
            'price': str(self.price),
            'discount_price': str(self.discount_price) if self.discount_price else None,
            'is_active': self.is_active,
        }

# Model for advertisement plan
class AdvertisementPlanPrice(models.Model):
    pricing_plan = models.ForeignKey(AdvertisementPlan, on_delete=models.CASCADE, related_name='advertisement_plan_prices')
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE, related_name='advertisement_currency_plan_prices')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_date = models.DateTimeField(default=timezone.now)
    last_modified = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('pricing_plan', 'currency')  # Ensures one price per plan per currency
        db_table = 'Advertisement Plan Price'
        verbose_name = "Advertisement Plan Price"  # Singular display name
        verbose_name_plural = "Advertisement Plan Price" # Plural display name

    def __str__(self):
        return f"{self.pricing_plan.plan_name} - {self.currency.currency_code} {self.price}"
    

    def to_dict(self):
        return {
            'id': self.id,
            'plan_name': self.pricing_plan.plan_name,
            'currency_name': self.currency.currency_name,
            'currency_code': self.currency.currency_code,
            'symbol': self.currency.symbol,
            'price': str(self.price),
            'discount_price': str(self.discount_price) if self.discount_price else None,
            'is_active': self.is_active,
        }


# Model for Listing Plan
class ListingPlanPayment(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('success', 'Success'),
        ('failed', 'Failed'),
        ('cancelled', 'Cancelled'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='listing_plan'
    )

    pricing_plan = models.ForeignKey(ListingPlanPrice, on_delete=models.SET_NULL, null=True)
    currency = models.ForeignKey(Currency, on_delete=models.SET_NULL, null=True)
    tool_ref_num = models.CharField(max_length=200, unique=True)
    tool_submission = models.ForeignKey('AITool', on_delete=models.SET_NULL, null=True, blank=True)
    is_active = models.BooleanField(default=True)

    # Payment Info
    payment_status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    payment_id = models.CharField(max_length=255, null=True, blank=True)       # Stripe: PaymentIntent ID / Razorpay: payment_id
    order_id = models.CharField(max_length=255, null=True, blank=True)         # Razorpay/PayPal order ID
    signature = models.CharField(max_length=512, null=True, blank=True)        # Razorpay signature or JWT/Hash from other gateway
    product_id = models.CharField(max_length=255, null=True, blank=True)       # If needed, for Stripe product or internal mapping
    invoice_url = models.URLField(null=True, blank=True)                       # Optional link to invoice

    # Pricing Info
    price_paid = models.DecimalField(max_digits=10, decimal_places=2)
    discount_applied = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user} - {self.pricing_plan.name if self.pricing_plan else ''} ({self.payment_status})"
    

    class Meta:
        db_table = 'Listing Plan Payment'
        verbose_name = "Listing Plan Payment"  # Singular display name
        verbose_name_plural = "Listing Plan Payment" # Plural display name
        indexes = [
        models.Index(fields=["user"]),
        models.Index(fields=["payment_id"]),
        models.Index(fields=["order_id"]),
    ]

    def to_dict(self):
        return {
            "user_id": self.user.id if self.user else None,
            "plan": self.pricing_plan.name if self.pricing_plan else None,
            "currency": self.currency.currency_code if self.currency else None,
            "price_paid": str(self.price_paid),
            "discount_applied": str(self.discount_applied) if self.discount_applied else None,
            "payment_status": self.payment_status,
            "payment_id": self.payment_id,
            "order_id": self.order_id,
            "signature": self.signature,
            "product_id": self.product_id,
            "invoice_url": self.invoice_url,
            "start_date": self.start_date.isoformat(),
            "end_date": self.end_date.isoformat(),
        }


# Model for Advertisement
class AdvertisementPlanPayment(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('success', 'Success'),
        ('failed', 'Failed'),
        ('cancelled', 'Cancelled'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='advertisement_plan'
    )

    pricing_plan = models.ForeignKey(AdvertisementPlanPrice, on_delete=models.SET_NULL, null=True)
    currency = models.ForeignKey(Currency, on_delete=models.SET_NULL, null=True)
    tool_ref_num = models.CharField(max_length=200, unique=True)
    tool_submission = models.ForeignKey(AITool, on_delete=models.SET_NULL, null=True, blank=True)
    is_active = models.BooleanField(default=True)

    # Payment Info
    payment_status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    payment_id = models.CharField(max_length=255, null=True, blank=True)       # Stripe: PaymentIntent ID / Razorpay: payment_id
    order_id = models.CharField(max_length=255, null=True, blank=True)         # Razorpay/PayPal order ID
    signature = models.CharField(max_length=512, null=True, blank=True)        # Razorpay signature or JWT/Hash from other gateway
    product_id = models.CharField(max_length=255, null=True, blank=True)       # If needed, for Stripe product or internal mapping
    invoice_url = models.URLField(null=True, blank=True)                       # Optional link to invoice

    # Pricing Info
    price_paid = models.DecimalField(max_digits=10, decimal_places=2)
    discount_applied = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    # Subscription Duration
    start_date = models.DateTimeField(default=timezone.now)
    end_date = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    def is_active(self):
        now = timezone.now()
        return self.payment_status == 'success' and self.start_date <= now <= self.end_date

    def __str__(self):
        return f"{self.user} - {self.pricing_plan.name if self.pricing_plan else ''} ({self.payment_status})"
    
    class Meta:
        db_table = 'Advertisement Plan Payment'
        verbose_name = "Advertisement Plan Payment"  # Singular display name
        verbose_name_plural = "Advertisement Plan Payment" # Plural display name
        indexes = [
        models.Index(fields=["user"]),
        models.Index(fields=["payment_id"]),
        models.Index(fields=["order_id"]),
    ]

    def to_dict(self):
        return {
            "user_id": self.user.id if self.user else None,
            "plan": self.pricing_plan.name if self.pricing_plan else None,
            "currency": self.currency.currency_code if self.currency else None,
            "price_paid": str(self.price_paid),
            "discount_applied": str(self.discount_applied) if self.discount_applied else None,
            "payment_status": self.payment_status,
            "payment_id": self.payment_id,
            "order_id": self.order_id,
            "signature": self.signature,
            "product_id": self.product_id,
            "invoice_url": self.invoice_url,
            "start_date": self.start_date.isoformat(),
            "end_date": self.end_date.isoformat(),
        }
  
class TooUpdatePricing(models.Model):
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE, related_name='update_price')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'TooUpdatePricing'
        verbose_name = "TooUpdatePricing"  # Singular display name
        verbose_name_plural = "TooUpdatePricing" # Plural display name
        ordering = ['-created_date']


    def __str__(self):
        return f"Currency Name: {self.currency.currency_name}, Currency Code: {self.current.currency_code}"
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.currency_name.currency_name,
            'price': self.price,
            'discount_price': self.discount_price,
        }
   

    

