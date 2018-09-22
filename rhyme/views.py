from django.http import HttpResponse
from django.shortcuts import render, render_to_response, redirect
from django.contrib.auth.decorators import login_required
import operator

def home(request):
    if request.user.is_authenticated:
        return redirect('/verses/index')
    else:
        return render(request, 'home.html')

def help(request):
    return render_to_response('help.html')

def privacy(request):
    return render_to_response('privacy.html')

def terms(request):
    return render_to_response('terms.html')
