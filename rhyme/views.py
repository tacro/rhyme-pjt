from django.http import HttpResponse
from django.shortcuts import render, render_to_response, redirect
from django.contrib.auth.decorators import login_required
from verses.models import Verse
import operator
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


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
    page = request.GET.get('page',1)
    if request.method == 'POST':
        if request.POST['w']:
            results_list = Verse.objects.filter(body__contains = request.POST['w']).order_by('-pub_date')
            paginator = Paginator(results_list, 15)
            try:
                results = paginator.page(page)
            except PageNotAnInteger:
                results = paginator.page(1)
            except EmptyPage:
                results = paginator.page(paginator.num_pages)
            return render(request, 'search.html', {'results': results})
        else:
            return render(request, 'search.html', {'error': 'Please enter some word'})
    else:
        trends_list = Verse.objects.order_by('-pub_date')
        paginator = Paginator(trends_list, 15)
        try:
            trends = paginator.page(page)
        except PageNotAnInteger:
            trends = paginator.page(1)
        except EmptyPage:
            trends = paginator.page(paginator.num_pages)
        return render(request, 'search.html', {'trends': trends})
