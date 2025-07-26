from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.views.generic.base import TemplateView
from django.views import View
from django.urls import reverse_lazy, reverse
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.http import JsonResponse, HttpResponse, Http404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q, F, Count, Avg, Max, Min
from django.db.models.functions import TruncDate
from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.cache import cache_page
from django.core.cache import cache
from django.contrib.auth.forms import UserCreationForm
from django.views import generic
import json
import datetime
from collections import defaultdict

from .models import Dare, Category, DifficultyLevel, DareCompletion, DareLike, SiteConfiguration
from .forms import DareForm, DareSearchForm, DareCompletionForm, ContactForm, NewsletterForm

class HomeView(TemplateView):
    template_name = 'home.html'

class DareDetailView(DetailView):
    model = Dare
    template_name = 'dare_detail.html'
    context_object_name = 'dare'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'

    def get_queryset(self):
        return Dare.objects.filter(is_approved=True).select_related(
            'category', 'difficulty'
        )
    
    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        obj.increment_views()
        return obj
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        context['completion_form'] = DareCompletionForm()
        context['recent_completions'] = DareCompletion.objects.filter(
            dare=self.object, is_verified=True
        ).order_by('-completed_at')[:5]
        
        context['user_has_liked'] = False
        context['related_dares'] = Dare.objects.filter(
            category=self.object.category,
            is_approved=True
        ).exclude(id=self.object.id).select_related(
            'category', 'difficulty'
        )[:4]
        
        total_attempts = DareCompletion.objects.filter(dare=self.object).count()
        verified_completions = DareCompletion.objects.filter(
            dare=self.object, is_verified=True
        ).count()
        
        if total_attempts > 0:
            context['completion_rate'] = round((verified_completions / total_attempts) * 100, 1)
        else:
            context['completion_rate'] = 0
            
        context['total_attempts'] = total_attempts
        
        return context

class DareCreateView(SuccessMessageMixin, CreateView):
    model = Dare
    form_class = DareForm
    template_name = 'dare_form.html'
    success_message = "🎉 Your dare has been submitted for review!"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = "Create a New Dare"
        context['page_description'] = "Fill out the form to submit a new dare to the exchange."
        return context

    def form_valid(self, form):
        config = SiteConfiguration.get_config()
        if config.require_approval:
            form.instance.status = 'pending'
        else:
            form.instance.status = 'approved'
            form.instance.is_approved = True
            form.instance.approved_at = timezone.now()
        
        response = super().form_valid(form)
        self.send_admin_notification()
        self.send_user_confirmation()
        
        return response
    
    def get_success_url(self):
        config = SiteConfiguration.get_config()
        if config.require_approval:
            messages.info(
                self.request, 
                "Your dare is under review and will be published once approved."
            )
            return reverse('dares:dare_list')
        else:
            return self.object.get_absolute_url()
    
    def send_admin_notification(self):
        try:
            subject = f"New Dare Submission: {self.object.title}"
            message = render_to_string('emails/admin_new_dare.txt', {
                'dare': self.object,
                'site_url': self.request.build_absolute_uri('/'),
            })
  
            admin_emails = ['admin@dareora.com']
            send_mail(
                subject=subject,
                message=message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=admin_emails,
                fail_silently=True,
            )
        except Exception as e:
            print(f"Failed to send admin notification: {e}")
    
    def send_user_confirmation(self):
        try:
            subject = f"Dare Submitted: {self.object.title}"
            message = render_to_string('emails/user_confirmation.txt', {
                'dare': self.object,
                'user_name': self.object.name,
                'site_url': self.request.build_absolute_uri('/'),
            })
            
            send_mail(
                subject=subject,
                message=message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[self.object.email],
                fail_silently=True,
            )
        except Exception as e:
            print(f"Failed to send user confirmation: {e}")

class DareUpdateView(SuccessMessageMixin, UpdateView):
    model = Dare
    form_class = DareForm
    template_name = 'dare_form.html'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
    success_message = "✅ Dare updated successfully!"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = "Edit Dare"
        context['page_description'] = "Make changes to the existing dare below."
        return context

    def get_queryset(self):
        return Dare.objects.all()
    
    def form_valid(self, form):
        form.instance.status = 'pending'
        form.instance.is_approved = False
        form.instance.is_featured = False
        return super().form_valid(form)

class DareDeleteView(DeleteView):
    model = Dare
    template_name = 'dare_confirm_delete.html'
    context_object_name = 'dare'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
    success_url = reverse_lazy('dares:dare_list')
    
    def get_queryset(self):
        return Dare.objects.all()
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, "🗑️ Dare deleted successfully.")
        return super().delete(request, *args, **kwargs)

class CategoryDetailView(ListView):
    model = Dare
    template_name = 'category_detail.html'
    context_object_name = 'dares'
    paginate_by = 12
    
    def get_queryset(self):
        self.category = get_object_or_404(Category, name=self.kwargs['category_name'])
        return Dare.objects.filter(
            category=self.category,
            is_approved=True
        ).select_related('category', 'difficulty').order_by('-created_at')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.category
        
        # Get category statistics
        context['category_stats'] = {
            'total_dares': self.get_queryset().count(),
            'avg_difficulty': self.get_queryset().aggregate(
                avg=Avg('difficulty__id')
            )['avg'] or 0,
            'most_popular': self.get_queryset().order_by('-views_count').first(),
        }
        
        return context

class DareCompletionCreateView(View):
    """Handle dare completion submissions via AJAX"""
    
    def post(self, request, slug):
        dare = get_object_or_404(Dare, slug=slug, is_approved=True)
        
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            form = DareCompletionForm(request.POST)
            
            if form.is_valid():
                completion = form.save(commit=False)
                completion.dare = dare
                
                # Check if user already completed this dare
                existing = DareCompletion.objects.filter(
                    dare=dare,
                    completer_email=completion.completer_email
                ).first()
                
                if existing:
                    return JsonResponse({
                        'success': False,
                        'error': 'You have already submitted a completion for this dare.'
                    })
                
                completion.save()
                dare.increment_completions()
                
                return JsonResponse({
                    'success': True,
                    'message': 'Completion submitted successfully! It will be reviewed and verified.',
                    'completions_count': dare.completions_count
                })
            else:
                return JsonResponse({
                    'success': False,
                    'errors': form.errors
                })
        
        return JsonResponse({'success': False, 'error': 'Invalid request'})

class DareLikeToggleView(View):
    """Handle dare likes via AJAX"""
    
    def post(self, request, slug):
        dare = get_object_or_404(Dare, slug=slug, is_approved=True)
        
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            # Simple email-based tracking (you might want to use sessions or user accounts)
            email = request.POST.get('email')
            if not email:
                return JsonResponse({'success': False, 'error': 'Email required'})
            
            like, created = DareLike.objects.get_or_create(
                dare=dare,
                user_email=email
            )
            
            if created:
                dare.increment_likes()
                liked = True
            else:
                like.delete()
                dare.likes_count = F('likes_count') - 1
                dare.save(update_fields=['likes_count'])
                liked = False
            
            # Refresh from database to get updated count
            dare.refresh_from_db()
            
            return JsonResponse({
                'success': True,
                'liked': liked,
                'likes_count': dare.likes_count
            })
        
        return JsonResponse({'success': False, 'error': 'Invalid request'})

class StatsView(TemplateView):
    """Display site statistics and analytics"""
    template_name = 'stats.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Overall statistics
        context['total_dares'] = Dare.objects.filter(is_approved=True).count()
        context['total_completions'] = DareCompletion.objects.filter(is_verified=True).count()
        context['total_likes'] = DareLike.objects.count()
        
        # Category breakdown
        context['category_stats'] = Category.objects.filter(is_active=True).annotate(
            dare_count=Count('dares', filter=Q(dares__is_approved=True)),
            completion_count=Count('dares__completions', filter=Q(dares__completions__is_verified=True)),
            likes_count=Count('dares__user_likes')
        ).order_by('-dare_count')
        
        # Difficulty breakdown
        context['difficulty_stats'] = DifficultyLevel.objects.annotate(
            dare_count=Count('dares', filter=Q(dares__is_approved=True)),
            avg_completions=Avg('dares__completions_count')
        ).order_by('id')
        
        # Monthly submission trends (last 12 months)
        twelve_months_ago = timezone.now() - datetime.timedelta(days=365)
        monthly_data = Dare.objects.filter(
            created_at__gte=twelve_months_ago,
            is_approved=True
        ).extra(
            select={'month': 'strftime("%%Y-%%m", created_at)'}
        ).values('month').annotate(
            count=Count('id')
        ).order_by('month')
        
        context['monthly_submissions'] = list(monthly_data)
        
        # Top performers
        context['most_viewed_dares'] = Dare.objects.filter(
            is_approved=True
        ).order_by('-views_count')[:10]
        
        context['most_liked_dares'] = Dare.objects.filter(
            is_approved=True
        ).order_by('-likes_count')[:10]
        
        context['most_completed_dares'] = Dare.objects.filter(
            is_approved=True
        ).order_by('-completions_count')[:10]
        
        return context

class AboutView(TemplateView):
    """About page with site information"""
    template_name = 'about.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['config'] = SiteConfiguration.get_config()
        return context

class ContactView(SuccessMessageMixin, View):
    """Contact page with form handling"""
    template_name = 'contact.html'
    success_message = "Message sent successfully! We'll get back to you soon."
    
    def get(self, request):
        form = ContactForm()
        return render(request, self.template_name, {'form': form})
    
    def post(self, request):
        form = ContactForm(request.POST)
        
        if form.is_valid():
            # Send email
            self.send_contact_email(form.cleaned_data)
            messages.success(request, self.success_message)
            return redirect('dares:contact')
        
        return render(request, self.template_name, {'form': form})
    
    def send_contact_email(self, data):
        """Send contact form email"""
        try:
            subject = f"Contact Form: {data['subject']}"
            message = render_to_string('emails/contact_form.txt', data)
            
            send_mail(
                subject=subject,
                message=message,
                from_email=data['email'],
                recipient_list=['contact@dareora.com'],  # Configure in settings
                fail_silently=True,
            )
        except Exception as e:
            print(f"Failed to send contact email: {e}")

class NewsletterSubscribeView(View):
    """Handle newsletter subscriptions via AJAX"""
    
    def post(self, request):
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            form = NewsletterForm(request.POST)
            
            if form.is_valid():
                email = form.cleaned_data['email']
                # Here you would typically save to a newsletter model or external service
                # For now, just return success
                
                return JsonResponse({
                    'success': True,
                    'message': 'Successfully subscribed to newsletter!'
                })
            else:
                return JsonResponse({
                    'success': False,
                    'errors': form.errors
                })
        
        return JsonResponse({'success': False, 'error': 'Invalid request'})

@method_decorator(cache_page(60 * 15), name='dispatch')  # Cache for 15 minutes
class APIStatsView(View):
    """JSON API endpoint for statistics (for charts/widgets)"""
    
    def get(self, request):
        stats = {
            'totals': {
                'dares': Dare.objects.filter(is_approved=True).count(),
                'completions': DareCompletion.objects.filter(is_verified=True).count(),
                'likes': DareLike.objects.count(),
                'categories': Category.objects.filter(is_active=True).count(),
            },
            'categories': list(Category.objects.filter(is_active=True).annotate(
                count=Count('dares', filter=Q(dares__is_approved=True))
            ).values('name', 'count')),
            'difficulties': list(DifficultyLevel.objects.annotate(
                count=Count('dares', filter=Q(dares__is_approved=True))
            ).values('name', 'count')),
        }
        
        return JsonResponse(stats)

class SearchSuggestionsView(View):
    def get(self, request, *args, **kwargs):
        query = request.GET.get('q', '')
        suggestions = []
        if query:
            dares = Dare.objects.filter(title__icontains=query)[:5]
            suggestions = [{'title': dare.title, 'url': dare.get_absolute_url()} for dare in dares]
        return JsonResponse({'suggestions': suggestions})

class DareListView(ListView):
    model = Dare
    template_name = 'dare_list.html'
    context_object_name = 'dares'
    paginate_by = 12
    
    def get_queryset(self):
        queryset = Dare.objects.filter(is_approved=True).select_related(
            'category', 'difficulty'
        )
        
        self.search_form = DareSearchForm(self.request.GET)
        
        if self.search_form.is_valid():
            search_query = self.search_form.cleaned_data.get('search')
            if search_query:
                queryset = queryset.filter(
                    Q(title__icontains=search_query) |
                    Q(dare_text__icontains=search_query)
                )
            
            # Filter by category
            category = self.search_form.cleaned_data.get('category')
            if category:
                queryset = queryset.filter(category=category)
    
            difficulty = self.search_form.cleaned_data.get('difficulty')
            if difficulty:
                queryset = queryset.filter(difficulty=difficulty)
            
            featured_only = self.search_form.cleaned_data.get('featured_only')
            if featured_only:
                queryset = queryset.filter(is_featured=True)

            sort_by = self.search_form.cleaned_data.get('sort_by')
            if sort_by == 'oldest':
                queryset = queryset.order_by('created_at')
            elif sort_by == 'most_viewed':
                queryset = queryset.order_by('-views_count', '-created_at')
            elif sort_by == 'most_liked':
                queryset = queryset.order_by('-likes_count', '-created_at')
            elif sort_by == 'title':
                queryset = queryset.order_by('title')
            else:  
                queryset = queryset.order_by('-created_at')
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if not hasattr(self, 'search_form'):
            self.search_form = DareSearchForm()
        
        context['search_form'] = self.search_form
        
        context['categories'] = Category.objects.filter(is_active=True).annotate(
            dare_count=Count('dares', filter=Q(dares__is_approved=True))
        )
        
        context['difficulties'] = DifficultyLevel.objects.annotate(
            dare_count=Count('dares', filter=Q(dares__is_approved=True))
        )
        
        return context

class CommunityView(ListView):
    """
    Display a board of recently completed and verified dares.
    """
    model = DareCompletion
    template_name = 'community.html'
    context_object_name = 'completions'
    paginate_by = 9

    def get_queryset(self):
        return DareCompletion.objects.filter(is_verified=True).select_related(
            'dare', 'dare__category'
        ).order_by('-completed_at')

class SignUpView(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'signup.html'
    
class PrivacyView(TemplateView):
    template_name = 'privacy.html'

class TermsView(TemplateView):
    template_name = 'terms.html'

class FAQView(TemplateView):
    template_name = 'faq.html'