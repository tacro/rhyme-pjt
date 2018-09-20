from django.contrib import admin
from django.urls import path, include
from rhyme import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('verses/', include('verses.urls')),
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('help/', views.help, name='help'),
    path('privacy/', views.privacy, name='privacy'),
    path('terms/', views.terms, name='terms'),
    path('rhymers/', include('users.urls')),
] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
