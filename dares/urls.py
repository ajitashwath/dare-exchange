from django.urls import path
from django.views.generic import TemplateView
from .views import (
    HomeView,
    DareListView,
    DareDetailView,
    DareCreateView,
    DareUpdateView,
    DareDeleteView,
    CategoryDetailView,
    DareCompletionCreateView,
    DareLikeToggleView,
    StatsView,
    AboutView,
    ContactView,
    NewsletterSubscribeView,
    APIStatsView,
    SearchSuggestionsView,
    CommunityView,
    chatbot_response
)

app_name = 'dares'

urlpatterns = [
    # Main pages
    path('', HomeView.as_view(), name='home'),
    path('dares/', DareListView.as_view(), name='dare_list'),
    path('community/', CommunityView.as_view(), name='community'),
    # This URL is for the 'Features' page, which uses the AboutView
    path('features/', AboutView.as_view(), name='about'),
    path('contact/', ContactView.as_view(), name='contact'),
    path('stats/', StatsView.as_view(), name='stats'),
    
    # Dare CRUD operations
    path('dare/new/', DareCreateView.as_view(), name='dare_create'),
    path('dare/<slug:slug>/', DareDetailView.as_view(), name='dare_detail'),
    path('dare/<slug:slug>/edit/', DareUpdateView.as_view(), name='dare_edit'),
    path('dare/<slug:slug>/delete/', DareDeleteView.as_view(), name='dare_delete'),
    
    # Category pages
    path('category/<str:category_name>/', CategoryDetailView.as_view(), name='category_detail'),
    
    # AJAX endpoints
    path('ajax/dare/<slug:slug>/complete/', DareCompletionCreateView.as_view(), name='dare_complete'),
    path('ajax/dare/<slug:slug>/like/', DareLikeToggleView.as_view(), name='dare_like'),
    path('ajax/newsletter/subscribe/', NewsletterSubscribeView.as_view(), name='newsletter_subscribe'),
    path('ajax/search/suggestions/', SearchSuggestionsView.as_view(), name='search_suggestions'),
    
    # API endpoints
    path('api/stats/', APIStatsView.as_view(), name='api_stats'),
    
    # Static pages (These are fine here if they are part of the 'dares' app context)
    path('privacy/', TemplateView.as_view(template_name='privacy.html'), name='privacy'),
    path('terms/', TemplateView.as_view(template_name='terms.html'), name='terms'),
    path('faq/', TemplateView.as_view(template_name='faq.html'), name='faq'),

    # Backend endpoint for the chatbot
    path('chatbot-response/', chatbot_response, name='chatbot_response'),
]