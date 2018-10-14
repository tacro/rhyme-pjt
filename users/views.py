from django.shortcuts import render, redirect, get_object_or_404
from .models import User, Relationship
from verses.models import Verse
from django.contrib.auth.decorators import login_required
# from django.contrib.auth.models import User
# notificatons
from notifications.signals import notify
from notifications.models import Notification
# infinite scroll
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def detail(request, user_id):
    user = get_object_or_404(User, pk = user_id)
    page = request.GET.get('page',1)
    posts_list = Verse.objects.filter(rhymer=user).order_by('-pub_date')
    paginator = Paginator(posts_list, 10)
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    followees = user.get_follows() # those who user follows
    followers = user.get_followers() # those who following user
    return render(request, 'users/detail.html', {'user':user, 'posts':posts, 'follows':len(followees), 'followers':len(followers)})

def likes(request, user_id):
    user = get_object_or_404(User, pk = user_id)
    page = request.GET.get('page',1)
    likes_list = Verse.objects.filter(likes = user).order_by('-pub_date')
    paginator = Paginator(likes_list, 10)
    try:
        likes = paginator.page(page)
    except PageNotAnInteger:
        likes = paginator.page(1)
    except EmptyPage:
        likes = paginator.page(paginator.num_pages)
    followees = user.get_follows() # those who user follows
    followers = user.get_followers() # those who following user
    return render(request, 'users/likes.html', {'user':user, 'likes':likes, 'follows':len(followees), 'followers':len(followers)})

@login_required
def edit(request, user_id):
    user = get_object_or_404(User, pk = user_id)
    if user == request.user:
        if request.method == 'POST':
            if request.POST['username']:
                user.username = request.POST['username']
            if request.POST['mcname']:
                user.mcname = request.POST['mcname']
            if request.POST['biography']:
                user.biography = request.POST['biography']
            if request.POST['email']:
                user.email = request.POST['email']
            if 'icon' in request.FILES:
                user.icon = request.FILES['icon']
            user.save()
            return redirect('/rhymers/' + str(user_id))
        else:
            return render(request, 'users/edit.html', {'user':user})
    else:
        return render(request, 'verses/index.html', {'error': 'You are not allowed to this page'})

@login_required
def follow(request, user_id):
    # specify who followee is
    followee = get_object_or_404(User, pk=user_id)
    # specify who follower is
    follower = request.user
    # make sure that they aren't identical
    if follower != followee:
        # check if that follower has already followed the user
        for followeeOfFollower in follower.get_follows():
            if followeeOfFollower == followee:
                # "do nothing and back to previous page
                return redirect('/verses/index')
        # make new relationship between them
        relationship = Relationship(follow = followee, follower = follower, )
        relationship.save()
        notify.send(follower, recipient = followee, verb = ' followed you:', action_object=follower, target=followee, description = 'follow')
        # back to previous page
        return redirect('/rhymers/' + str(user_id))
    else:
        return redirect('/verses/index')

@login_required
def unfollow(request, user_id):
    followee = get_object_or_404(User, pk=user_id)
    follower = request.user
    relationship = Relationship.objects.filter(follow = followee, follower = follower)
    if relationship:
        relationship.delete()
        return redirect('/rhymers/' + str(user_id))
    else:
        return redirect('/verses/index')

def show_follows(request, user_id):
    user = get_object_or_404(User, pk = user_id)
    page = request.GET.get('page',1)
    # get those who user follows
    followees_list = user.get_follows()
    paginator = Paginator(followees_list, 10)
    try:
        followees = paginator.page(page)
    except PageNotAnInteger:
        followees = paginator.page(1)
    except EmptyPage:
        followees = paginator.page(paginator.num_pages)
    return render(request, 'users/show_follows.html', {'followees':followees})


def show_followers(request, user_id):
    user = get_object_or_404(User, pk = user_id)
    page = request.GET.get('page',1)
    # get those who follow user
    followers_list = user.get_followers()
    paginator = Paginator(followers_list, 10)
    try:
        followers = paginator.page(page)
    except PageNotAnInteger:
        followers = paginator.page(1)
    except EmptyPage:
        followers = paginator.page(paginator.num_pages)
    return render(request, 'users/show_followers.html', {'followers':followers})

@login_required
def notification(request, user_id):
    user = get_object_or_404(User, pk = user_id)
    if user == request.user:
        notifications_list = Notification.objects.filter(recipient = user).order_by('-timestamp')
        page = request.GET.get('page',1)
        paginator = Paginator(notifications_list, 8)
        try:
            notifications = paginator.page(page)
        except PageNotAnInteger:
            notifications = paginator.page(1)
        except EmptyPage:
            notifications = paginator.page(paginator.num_pages)
        return render(request, 'users/notification.html', {'user':user, 'notifications':notifications})
    else:
        return render(request, 'verses/index.html', {'error': 'You are not allowed to this page'})
