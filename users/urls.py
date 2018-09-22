from django.urls import path
from . import views

app_name = 'users' 

urlpatterns = [
    path('<int:user_id>',  views.detail, name = 'detail'),
    path('<int:user_id>/edit', views.edit, name = 'edit'),
    path('<int:user_id>/follow', views.follow, name = 'follow'),
    path('<int:user_id>/unfollow', views.unfollow, name = 'unfollow'),
    path('<int:user_id>/followers', views.show_followers, name = 'followers'),
    path('<int:user_id>/follows', views.show_follows, name = 'follows'),
]
