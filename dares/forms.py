from django import forms
from django.core.exceptions import ValidationError
from .models import Dare, Category, DifficultyLevel, DareCompletion, DareLike

class DareForm(forms.ModelForm):
    class Meta:
        model = Dare
        fields = [
            'title', 'name', 'email', 'phone_number', 'college',
            'category', 'difficulty', 'dare_text', 'estimated_time',
            'required_items', 'safety_notes'
        ]
        
        widgets = {
            'title': forms.TextInput(attrs={
                'placeholder': 'e.g., Sing a song in the college cafeteria',
                'class': 'form-control',
            }),
            'name': forms.TextInput(attrs={
                'placeholder': 'e.g., Priya Singh',
                'class': 'form-control',
            }),
            'email': forms.EmailInput(attrs={
                'placeholder': 'e.g., priya@example.com',
                'class': 'form-control',
            }),
            'phone_number': forms.TextInput(attrs={
                'placeholder': 'e.g., +91-9876543210',
                'class': 'form-control',
            }),
            'college': forms.TextInput(attrs={
                'placeholder': 'e.g., Lovely Professional University',
                'class': 'form-control',
            }),
            'category': forms.Select(attrs={
                'class': 'form-control',
            }),
            'difficulty': forms.Select(attrs={
                'class': 'form-control',
            }),
            'dare_text': forms.Textarea(attrs={
                'placeholder': 'Describe the dare in detail. Be specific about what needs to be done, where, and any special requirements...',
                'rows': 6,
                'class': 'form-control',
            }),
            'estimated_time': forms.NumberInput(attrs={
                'placeholder': 'e.g., 15 (minutes)',
                'class': 'form-control',
                'min': '1',
                'max': '1440',
            }),
            'required_items': forms.Textarea(attrs={
                'placeholder': 'List any items, props, or materials needed (optional)...',
                'rows': 3,
                'class': 'form-control',
            }),
            'safety_notes': forms.Textarea(attrs={
                'placeholder': 'Any safety precautions, warnings, or age restrictions (optional)...',
                'rows': 3,
                'class': 'form-control',
            }),
        }
        
        labels = {
            'title': 'Dare Title',
            'name': 'Your Full Name',
            'email': 'Email Address',
            'phone_number': 'Phone Number',
            'college': 'College/University',
            'category': 'Dare Category',
            'difficulty': 'Difficulty Level',
            'dare_text': 'Dare Description',
            'estimated_time': 'Estimated Time (minutes)',
            'required_items': 'Required Items',
            'safety_notes': 'Safety Notes',
        }
        
        help_texts = {
            'title': 'Give your dare a catchy, descriptive title',
            'phone_number': 'Used for verification only, not displayed publicly',
            'estimated_time': 'How long do you think this dare will take to complete?',
            'required_items': 'What items or materials are needed for this dare?',
            'safety_notes': 'Any important safety information or warnings',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.fields['category'].empty_label = "Select a category"
        self.fields['difficulty'].empty_label = "Select difficulty level"
        
        self.fields['title'].required = True
        self.fields['category'].required = True
        self.fields['difficulty'].required = True
        
        for field_name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})
            if field.required:
                field.widget.attrs.update({'required': True})

    def clean_title(self):
        title = self.cleaned_data.get('title')
        if title:
            inappropriate_words = ['hate', 'violence', 'illegal', 'drugs']
            title_lower = title.lower()
            for word in inappropriate_words:
                if word in title_lower:
                    raise ValidationError(f"Title contains inappropriate content: '{word}'")
            
            if not self.instance.pk:
                if Dare.objects.filter(title__iexact=title).exists():
                    raise ValidationError("A dare with this title already exists. Please choose a different title.")
        
        return title

    def clean_phone_number(self):
        phone = self.cleaned_data.get('phone_number')
        if phone:
            phone_clean = phone.replace(' ', '').replace('-', '')
            if not phone_clean.startswith('+'):
                phone_clean = '+91' + phone_clean
            return phone_clean
        return phone

    def clean_estimated_time(self):
        time = self.cleaned_data.get('estimated_time')
        if time and time > 1440: 
            raise ValidationError("Estimated time cannot exceed 24 hours (1440 minutes)")
        return time

class DareSearchForm(forms.Form):
    SORT_CHOICES = [
        ('newest', 'Newest First'),
        ('oldest', 'Oldest First'),
        ('most_viewed', 'Most Viewed'),
        ('most_liked', 'Most Liked'),
        ('title', 'Title A-Z'),
    ]
    
    search = forms.CharField(
        max_length=200,
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': 'Search dares...',
            'class': 'form-control search-input',
        })
    )
    
    category = forms.ModelChoiceField(
        queryset=Category.objects.filter(is_active=True),
        required=False,
        empty_label="All Categories",
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    difficulty = forms.ModelChoiceField(
        queryset=DifficultyLevel.objects.all(),
        required=False,
        empty_label="All Difficulties",
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    sort_by = forms.ChoiceField(
        choices=SORT_CHOICES,
        required=False,
        initial='newest',
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    featured_only = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )

class DareCompletionForm(forms.ModelForm):
    class Meta:
        model = DareCompletion
        fields = ['completer_name', 'completer_email', 'completion_proof', 'completion_image']
        
        widgets = {
            'completer_name': forms.TextInput(attrs={
                'placeholder': 'Your full name',
                'class': 'form-control',
            }),
            'completer_email': forms.EmailInput(attrs={
                'placeholder': 'your.email@example.com',
                'class': 'form-control',
            }),
            'completion_proof': forms.Textarea(attrs={
                'placeholder': 'Tell us how you completed this dare! Be detailed...',
                'rows': 4,
                'class': 'form-control',
            }),
            'completion_image': forms.URLInput(attrs={
                'placeholder': 'https://imgur.com/your-image (optional)',
                'class': 'form-control',
            }),
        }
        
        labels = {
            'completer_name': 'Your Name',
            'completer_email': 'Email Address', 
            'completion_proof': 'How did you complete this dare?',
            'completion_image': 'Proof Image/Video URL',
        }
        
        help_texts = {
            'completion_proof': 'Describe in detail how you completed the dare',
            'completion_image': 'Optional: Link to image or video proof (use imgur, youtube, etc.)',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})

class ContactForm(forms.Form):
    SUBJECT_CHOICES = [
        ('general', 'General Inquiry'),
        ('submission', 'Dare Submission Issue'),
        ('report', 'Report Inappropriate Content'),
        ('technical', 'Technical Issue'),
        ('partnership', 'Partnership/Collaboration'),
    ]
    
    name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'placeholder': 'Your full name',
            'class': 'form-control',
        })
    )
    
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'placeholder': 'your.email@example.com',
            'class': 'form-control',
        })
    )
    
    subject = forms.ChoiceField(
        choices=SUBJECT_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    message = forms.CharField(
        widget=forms.Textarea(attrs={
            'placeholder': 'Your message...',
            'rows': 5,
            'class': 'form-control',
        })
    )
    
    def clean_message(self):
        message = self.cleaned_data.get('message')
        if message and len(message) < 10:
            raise ValidationError("Message must be at least 10 characters long.")
        return message

class NewsletterForm(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'placeholder': 'Enter your email address',
            'class': 'form-control newsletter-input',
        })
    )
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        return email

class BulkActionForm(forms.Form):
    """Form for bulk actions on dares (admin use)"""
    
    ACTION_CHOICES = [
        ('approve', 'Approve Selected'),
        ('reject', 'Reject Selected'),
        ('feature', 'Feature Selected'),
        ('delete', 'Delete Selected'),
    ]
    
    action = forms.ChoiceField(
        choices=ACTION_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    selected_dares = forms.CharField(
        widget=forms.HiddenInput()
    )
    
    rejection_reason = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'placeholder': 'Reason for rejection (optional)',
            'rows': 3,
            'class': 'form-control',
        })
    )