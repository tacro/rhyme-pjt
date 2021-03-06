from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from verses.models import Verse
from users.models import User
import operator
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from itertools import chain


def home(request):
    if request.user.is_authenticated:
        user = request.user
        followees = user.get_follows();
        verse_list = Verse.objects.filter(rhymer = user)
        for followee in followees:
            followee_verses = Verse.objects.filter(rhymer = followee)
            verse_list = list(chain(verse_list, followee_verses))
        if len(verse_list) == 0:
            return redirect('/verses/index')
        verse_list = sorted(verse_list, key = operator.attrgetter('pub_date'), reverse = True)
        page = request.GET.get('page',1)
        paginator = Paginator(verse_list, 15)
        try:
            verses = paginator.page(page)
        except PageNotAnInteger:
            verses = paginator.page(1)
        except EmptyPage:
            verses = paginator.page(paginator.num_pages)
        return render(request, 'timeline.html', {'verses':verses})
    else:
        return render(request, 'home.html')

def help(request):
    return render(request, 'help.html')

def privacy(request):
    return render(request,'privacy.html')

def terms(request):
    return render(request, 'terms.html')

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
