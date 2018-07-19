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
    path('rhymers/', include('users.urls')),
] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
