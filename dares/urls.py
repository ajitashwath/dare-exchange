from django.urls import path
from .views import (
    DareListView,
    DareDetailView,
    DareCreateView,
    DareUpdateView,
    DareDeleteView,
)

urlpatterns = [
    path('', DareListView.as_view(), name='dare_list'),
    path('dare/<int:pk>/', DareDetailView.as_view(), name='dare_detail'),
    path('dare/new/', DareCreateView.as_view(), name='dare_new'),
    path('dare/<int:pk>/edit/', DareUpdateView.as_view(), name='dare_edit'),
    path('dare/<int:pk>/delete/', DareDeleteView.as_view(), name='dare_delete'),
]