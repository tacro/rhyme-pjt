from django.shortcuts import render, redirect, get_object_or_404
from .models import User
from django.contrib.auth.decorators import login_required


def detail(request, user_id):
    user = get_object_or_404(User, pk = user_id)
    return render(request, 'users/detail.html', {'user':user})

@login_required
def edit(request, user_id):
    user = get_object_or_404(User, pk = user_id)
    return render(request, 'users/edit.html', {'user':user})
