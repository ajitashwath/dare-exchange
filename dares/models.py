from django.db import models
from django.urls import reverse
from django.core.validators import RegexValidator
from django.contrib.auth.models import User
from django.utils.text import slugify
import uuid

class Category(models.Model):
    CATEGORY_CHOICES = [
        ('extreme', 'Extreme'),
        ('creative', 'Creative'),
        ('social', 'Social'),
        ('adventure', 'Adventure'),
    ]
    
    CATEGORY_ICONS = {
        'extreme': 'ph-flame',
        'creative': 'ph-paint-brush',
        'social': 'ph-users',
        'adventure': 'ph-mountains',
    }
    
    CATEGORY_COLORS = {
        'extreme': '#EF4444',
        'creative': '#8B5CF6',
        'social': '#06B6D4',
        'adventure': '#F59E0B',
    }
    
    name = models.CharField(max_length=50, choices=CATEGORY_CHOICES, unique=True)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = "Categories"
        ordering = ['name']
    
    def __str__(self):
        return self.get_name_display()
    
    @property
    def icon(self):
        return self.CATEGORY_ICONS.get(self.name, 'ph-question')
    
    @property
    def color(self):
        return self.CATEGORY_COLORS.get(self.name, '#6B7280')
    
    @property
    def dare_count(self):
        return self.dares.filter(is_approved=True).count()

class DifficultyLevel(models.Model):
    DIFFICULTY_CHOICES = [
        ('easy', 'Easy'),
        ('medium', 'Medium'),
        ('hard', 'Hard'),
        ('extreme', 'Extreme'),
    ]
    
    name = models.CharField(max_length=20, choices=DIFFICULTY_CHOICES, unique=True)
    description = models.TextField(blank=True)
    color = models.CharField(max_length=7, default='#6B7280')
    
    def __str__(self):
        return self.get_name_display()
    
    class Meta:
        ordering = ['name']

class Dare(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending Review'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('featured', 'Featured'),
    ]
    
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."
    )
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=200, help_text="Give your dare a catchy title")
    slug = models.SlugField(unique=True, blank=True)
    
    name = models.CharField(max_length=100, help_text="Your full name")
    email = models.EmailField(help_text="Your email address")
    phone_number = models.CharField(
        validators=[phone_regex], 
        max_length=17, 
        help_text="Your phone number for verification"
    )
    college = models.CharField(max_length=200, help_text="Your college/university name")
    
    dare_text = models.TextField(help_text="Describe the dare in detail")
    category = models.ForeignKey(
        Category, 
        on_delete=models.CASCADE, 
        related_name='dares',
        help_text="Select the appropriate category"
    )
    difficulty = models.ForeignKey(
        DifficultyLevel, 
        on_delete=models.CASCADE, 
        related_name='dares',
        help_text="How difficult is this dare?"
    )
    
    estimated_time = models.PositiveIntegerField(
        help_text="Estimated time to complete (in minutes)", 
        null=True, 
        blank=True
    )
    required_items = models.TextField(
        blank=True, 
        help_text="List any items/materials needed (optional)"
    )
    safety_notes = models.TextField(
        blank=True, 
        help_text="Any safety precautions or warnings (optional)"
    )
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    is_approved = models.BooleanField(default=False)
    is_featured = models.BooleanField(default=False)
    rejection_reason = models.TextField(blank=True)
    
    views_count = models.PositiveIntegerField(default=0)
    likes_count = models.PositiveIntegerField(default=0)
    completions_count = models.PositiveIntegerField(default=0)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    approved_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['status', 'is_approved']),
            models.Index(fields=['category', 'difficulty']),
            models.Index(fields=['-created_at']),
        ]

    def __str__(self):
        return f"{self.title} by {self.name}"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
            original_slug = self.slug
            counter = 1
            while Dare.objects.filter(slug=self.slug).exists():
                self.slug = f"{original_slug}-{counter}"
                counter += 1
        
        if self.status == 'approved':
            self.is_approved = True
            if not self.approved_at:
                from django.utils import timezone
                self.approved_at = timezone.now()
        elif self.status == 'featured':
            self.is_approved = True
            self.is_featured = True
            if not self.approved_at:
                from django.utils import timezone
                self.approved_at = timezone.now()
        else:
            self.is_approved = False
            self.is_featured = False
            
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('dares:dare_detail', kwargs={'slug': self.slug})
    
    @property
    def difficulty_badge_color(self):
        colors = {
            'easy': '#10B981',
            'medium': '#F59E0B', 
            'hard': '#EF4444',
            'extreme': '#7C2D12'
        }
        return colors.get(self.difficulty.name, '#6B7280')
    
    def increment_views(self):
        self.views_count += 1
        self.save(update_fields=['views_count'])
    
    def increment_likes(self):
        self.likes_count += 1
        self.save(update_fields=['likes_count'])
    
    def increment_completions(self):
        self.completions_count += 1
        self.save(update_fields=['completions_count'])

class DareCompletion(models.Model):
    dare = models.ForeignKey(Dare, on_delete=models.CASCADE, related_name='completions')
    completer_name = models.CharField(max_length=100)
    completer_email = models.EmailField()
    completion_proof = models.TextField(help_text="Describe how you completed the dare")
    completion_image = models.URLField(blank=True, help_text="Link to image/video proof (optional)")
    completed_at = models.DateTimeField(auto_now_add=True)
    is_verified = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['-completed_at']
        unique_together = ['dare', 'completer_email']
    
    def __str__(self):
        return f"{self.completer_name} completed '{self.dare.title}'"

class DareLike(models.Model):
    dare = models.ForeignKey(Dare, on_delete=models.CASCADE, related_name='user_likes')
    user_email = models.EmailField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['dare', 'user_email']
    
    def __str__(self):
        return f"Like on '{self.dare.title}'"

class SiteConfiguration(models.Model):
    site_name = models.CharField(max_length=100, default="Dareora")
    site_tagline = models.CharField(max_length=200, default="Dive into the art of daring")
    site_description = models.TextField(default="Where innovative social technology meets thrilling experiences")
    allow_submissions = models.BooleanField(default=True)
    require_approval = models.BooleanField(default=True)
    enable_likes = models.BooleanField(default=True)
    enable_completions = models.BooleanField(default=True)
    
    max_dares_per_user = models.PositiveIntegerField(default=5)
    featured_dares_count = models.PositiveIntegerField(default=6)
    
    class Meta:
        verbose_name = "Site Configuration"
        verbose_name_plural = "Site Configuration"
    
    def __str__(self):
        return self.site_name
    
    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)
    
    @classmethod
    def get_config(cls):
        config, created = cls.objects.get_or_create(pk=1)
        return config