from django.http import HttpResponse
from django.shortcuts import render, render_to_response, redirect
from django.contrib.auth.decorators import login_required
from verses.models import Verse
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

def search(request):
    if request.method == 'POST':
        if request.POST['w']:
            results = Verse.objects.filter(body__contains = request.POST['w']).order_by('-pub_date')
            return render(request, 'search.html', {'results': results})
        else:
            return render(request, 'search.html', {'error': 'Please enter some word'})
    else:
        trends = Verse.objects.order_by('-pub_date')
        return render(request, 'search.html', {'trends': trends})
