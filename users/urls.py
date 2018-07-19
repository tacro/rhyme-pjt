from django.urls import path
from . import views

urlpatterns = [
    path('<int:user_id>',  views.detail, name = 'detail'),
    path('<int:user_id>/edit', views.edit, name = 'edit'),
]
