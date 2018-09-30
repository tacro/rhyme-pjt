from django.contrib import admin
from django.urls import path, include
from rhyme import views
from django.conf import settings
from django.conf.urls.static import static
import notifications.urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('verses/', include('verses.urls')),
    path('rhymers/', include('users.urls')),
    path('notifications/', include('notifications.urls')),
    path('', views.home, name='home'),
    path('help/', views.help, name='help'),
    path('privacy/', views.privacy, name='privacy'),
    path('terms/', views.terms, name='terms'),
    path('search/', views.search, name='search'),
] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
