from django.urls import path
from . import views
from .views import PostLikeToggle, PostLikeAPIToggle

app_name = 'verses'

urlpatterns = [
    path('create/',  views.create, name = 'create'),
    path('index/', views.index, name='index'),
    path('<int:verse_id>',views.detail, name='detail'),
    path('<int:verse_id>/like/',PostLikeToggle.as_view(), name='like'),
    path('api/<int:verse_id>/like/',PostLikeAPIToggle.as_view(), name='like-api'),
    path('<int:verse_id>/answer/',views.answer, name = 'answer'),
    path('<int:verse_id>/beef/',views.beef, name = 'beef'),
]
