from django.shortcuts import render, redirect, get_object_or_404
from .models import User, Relationship
from verses.models import Verse
from django.contrib.auth.decorators import login_required
# from django.contrib.auth.models import User


def detail(request, user_id):
    user = get_object_or_404(User, pk = user_id)
    posts = Verse.objects.filter(rhymer=user)
    followees = user.get_follows() # those who user follows
    followers = user.get_followers() # those who following user
    return render(request, 'users/detail.html', {'user':user, 'posts':posts, 'follows':len(followees), 'followers':len(followers)})

@login_required
def edit(request, user_id):
    user = get_object_or_404(User, pk = user_id)
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
    # get those who user follows
    followees = user.get_follows()
    return render(request, 'users/show_follows.html', {'followees':followees})


def show_followers(request, user_id):
    user = get_object_or_404(User, pk = user_id)
    # get those who follow user
    followers = user.get_followers()
    return render(request, 'users/show_followers.html', {'followers':followers})
