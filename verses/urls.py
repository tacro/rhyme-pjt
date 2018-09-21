from django.urls import path
from . import views
from .views import PostLikeToggle, PostLikeAPIToggle

urlpatterns = [
    path('create/',  views.create, name = 'create'),
    path('index/', views.index, name='index'),
    path('<int:verse_id>',views.detail, name='detail'),
    path('<int:verse_id>/like/',PostLikeToggle.as_view(), name='like'),
    path('api/<int:verse_id>/like/',PostLikeAPIToggle.as_view(), name='like-api'),
    path('<int:verse_id>/answer/',views.answer, name = 'answer'),
]
