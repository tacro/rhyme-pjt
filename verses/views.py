from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.generic import RedirectView
from .models import Verse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
from django.contrib.auth.models import User


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

# First I have to write verse/detail page

def detail(request, verse_id):
    verse = get_object_or_404(Verse, pk = verse_id)
    return render(request, 'verses/detail.html', {'verse':verse})

@login_required
def answer(request, verse_id):
    target = get_object_or_404(Verse, pk = verse_id)
    if request.method == 'POST':
        if request.POST['body']:
            verse = Verse()
            verse.body = request.POST['body']
            verse.rhymer = request.user
            verse.target = target
            verse.type = 1
            verse.save()
            return redirect('index')
        else:
            return render(request, 'verses/answer.html', {'error': 'Something went wrong'})
    else:
        print('verse_id : %d' % verse_id)
        return render(request, 'verses/answer.html', {'target':target})

@login_required
def beef(request, verse_id):
    target = get_object_or_404(Verse, pk = verse_id)
    if request.method == 'POST':
        if request.POST['body']:
            verse = Verse()
            verse.body = request.POST['body']
            verse.rhymer = request.user
            verse.target = target
            verse.type = 2
            verse.save()
            return redirect('index')
        else:
            return render(request, 'verses/beef.html', {'error': 'Something went wrong'})
    else:
        print('verse_id : %d' % verse_id)
        return render(request, 'verses/beef.html', {'target':target})


class PostLikeToggle(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        verse_id = self.kwargs.get("verse_id")
        verse = get_object_or_404(Verse, pk=verse_id)
        url_ = verse.get_absolute_url()
        user = self.request.user
        if user.is_authenticated:
            if user in verse.likes.all():
                verse.likes.remove(user)
            else:
                verse.likes.add(user)
        return url_


class PostLikeAPIToggle(APIView):
    authentication_classes = (authentication.SessionAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, verse_id = None, format=None):
        # verse_id = self.kwargs.get("verse_id")
        verse = get_object_or_404(Verse, pk=verse_id)
        url_ = verse.get_absolute_url()
        user = self.request.user
        updated = False
        liked = False
        if user.is_authenticated:
            if user in verse.likes.all():
                liked = False
                verse.likes.remove(user)
            else:
                liked = True
                verse.likes.add(user)
            updated = True
        data = {
            "updated": updated,
            "liked": liked,
        }
        return Response(data)
