from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from dares import views as dare_views
from dares.forms import CustomLoginForm

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('dares.urls')),
    path('login/', auth_views.LoginView.as_view(template_name='login.html', authentication_form=CustomLoginForm), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('signup/', dare_views.SignUpView.as_view(), name='signup'),
    path('accounts/', include('allauth.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)