from django.shortcuts import render
from .models import Verse

def create(request):
    return render(request, 'verses/create.html')
