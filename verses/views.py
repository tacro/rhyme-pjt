from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.generic import RedirectView
from .models import Verse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
from django.contrib.auth.models import User
# To post verses to Twitter
from requests_oauthlib import OAuth1Session
import json
from allauth.socialaccount.models import SocialToken, SocialAccount, SocialApp


@login_required
def create(request):
    if request.method == 'POST':
        if request.POST['body']:
            verse = Verse()
            verse.body = request.POST['body']
            verse.rhymer = request.user
            verse.save()
            # if user is associated with twitter
            # specify the uesr's twitter account
            twitterAccount = get_object_or_404(SocialAccount, user = request.user)
            if twitterAccount:
                # post to twitter
                # specify the app from SocialApp objs (by what?)
                twitterApp = get_object_or_404(SocialApp, name = 'twitter')
                # to authenticate, get client_id and secret key of app and access key and secret key of account
                accessTokenSecret = SocialToken.objects.filter(account__user=request.user, account__provider='twitter')
                twitter = OAuth1Session(twitterApp.client_id, twitterApp.secret, twitterAccount.uid, accessTokenSecret)
                tweet = verse.body + " #rhyme"
                params = {"status": tweet}
                req = twitter.post("https://api.twitter.com/1.1/statuses/update.json",params = params)
            return redirect('/verses/index')
        else:
            return render(request, 'verses/create.html', {'error': 'Please enter your verse'})
    else:
        return render(request, 'verses/create.html')

def index(request):
    verses = Verse.objects.order_by('-pub_date')
    return render(request, 'verses/index.html', {'verses':verses})

# First I have to write verse/detail page

def detail(request, verse_id):
    verse = get_object_or_404(Verse, pk = verse_id)
    answers = verse.get_answers().order_by('-pub_date')
    beefs = verse.get_beefs().order_by('-pub_date')
    return render(request, 'verses/detail.html', {'verse':verse, 'answers':answers, 'beefs':beefs})

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
            return redirect('/verses/index')
        else:
            return render(request, 'verses/answer.html', {'error': 'Something went wrong'})
    else:
        answers = target.get_answers().order_by('-pub_date')
        return render(request, 'verses/answer.html', {'target':target, 'answers':answers})

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
            return redirect('/verses/index')
        else:
            return render(request, 'verses/beef.html', {'error': 'Something went wrong'})
    else:
        beefs = target.get_beefs().order_by('-pub_date')
        return render(request, 'verses/beef.html', {'target':target, 'beefs':beefs})


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
