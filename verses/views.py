from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Verse

@login_required
def create(request):
    if request.method == 'POST':
        if request.POST['body']:
            verse = Verse()
            verse.body = request.POST['body']
            verse.rhymer = request.user
            verse.save()
            return redirect('index')
        else:
            return render(request, 'verses/create.html', {'error': 'Please enter your verse'})
    else:
        return render(request, 'verses/create.html')

def index(request):
    verses = Verse.objects
    return render(request, 'verses/index.html', {'verses':verses})
