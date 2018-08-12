from django.urls import path
from . import views
from .views import PostLikeRedirect

urlpatterns = [
    path('create/',  views.create, name = 'create'),
    path('index/', views.index, name='index'),
    path('<int:verse_id>',views.detail, name='detail'),
    # path('<int:product_id>',  views.detail, name = 'detail'),
    # path('<int:product_id>/upvote',  views.upvote, name = 'upvote'),
]
