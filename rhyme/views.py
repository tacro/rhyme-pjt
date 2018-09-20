from django.http import HttpResponse
from django.shortcuts import render, render_to_response
from django.contrib.auth.decorators import login_required
import operator

@login_required
def home(request):
    return render(request, 'home.html')

def about(request):
    return render_to_response('about.html')

def help(request):
    return render_to_response('help.html')

def privacy(request):
    return render_to_response('privacy.html')

def terms(request):
    return render_to_response('terms.html')
