from django.shortcuts import render, redirect, get_object_or_404
from .models import User
from verses.models import Verse
from django.contrib.auth.decorators import login_required


def detail(request, user_id):
    user = get_object_or_404(User, pk = user_id)
    posts = Verse.objects.filter(rhymer=user)
    return render(request, 'users/detail.html', {'user':user, 'posts':posts})

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
