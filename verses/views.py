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
# notificatons
from notifications.signals import notify
# infinite scroll
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


@login_required
def create(request):
    if request.method == 'POST':
        if request.POST['body']:
            verse = Verse()
            verse.body = request.POST['body']
            verse.rhymer = request.user
            verse.save()
            # if user chose to share post on twitter
            if request.POST.get('tweetBtn', False):
                # specify the uesr's twitter account
                # if request.POST['tweetBtn'] == 1:
                twitterAccount = get_object_or_404(SocialAccount, user = request.user, provider = 'twitter')
                if twitterAccount:
                    # post to twitter
                    # specify the app from SocialApp objs (by what?)
                    twitterApp = get_object_or_404(SocialApp, name = 'twitter')
                    # to authenticate, get client_id and secret key of app and access key and secret key of account
                    accessToken = get_object_or_404(SocialToken, app = twitterApp, account = twitterAccount)
                    twitter = OAuth1Session(twitterApp.client_id, twitterApp.secret, accessToken.token, accessToken.token_secret)
                    tweet = verse.tweet() + "\n#rhymeyourvibes http://rhyme.live/verses/{}".format(verse.id)
                    params = {"status": tweet}
                    req = twitter.post("https://api.twitter.com/1.1/statuses/update.json",params = params)
                # if twitterAccount doesn't exist, associate it first.
            return redirect('/verses/index')
        else:
            return render(request, 'verses/create.html', {'error': 'Please enter your verse'})
    else:
        return render(request, 'verses/create.html')

def index(request):
    verses_list = Verse.objects.order_by('-pub_date')
    page = request.GET.get('page',1)
    paginator = Paginator(verses_list, 10)
    try:
        verses = paginator.page(page)
    except PageNotAnInteger:
        verses = paginator.page(1)
    except EmptyPage:
        verses = paginator.page(paginator.num_pages)
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
            if request.POST.get('tweetBtn', False):
                # specify the uesr's twitter account
                # if request.POST['tweetBtn'] == 1:
                twitterAccount = get_object_or_404(SocialAccount, user = request.user, provider = 'twitter')
                if twitterAccount:
                    # post to twitter
                    # specify the app from SocialApp objs (by what?)
                    twitterApp = get_object_or_404(SocialApp, name = 'twitter')
                    # to authenticate, get client_id and secret key of app and access key and secret key of account
                    accessToken = get_object_or_404(SocialToken, app = twitterApp, account = twitterAccount)
                    twitter = OAuth1Session(twitterApp.client_id, twitterApp.secret, accessToken.token, accessToken.token_secret)
                    if target.rhymer.mcname:
                        tweet = "Answering to " + target.rhymer.mcname + "'s verse:\n" + verse.tweet() + "\n#rhymeyourvibes http://rhyme.live/verses/{}".format(verse.id)
                    else:
                        tweet = "Answering to " + target.rhymer.username + "'s verse:\n" + verse.tweet() + "\n#rhymeyourvibes http://rhyme.live/verses/{}".format(verse.id)
                    params = {"status": tweet}
                    req = twitter.post("https://api.twitter.com/1.1/statuses/update.json",params = params)
            notify.send(request.user, recipient = target.rhymer, verb = ' answered to you:', action_object=verse, target=target, description = 'answer')
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
            if request.POST.get('tweetBtn', False):
                # specify the uesr's twitter account
                # if request.POST['tweetBtn'] == 1:
                twitterAccount = get_object_or_404(SocialAccount, user = request.user, provider = 'twitter')
                if twitterAccount:
                    # post to twitter
                    # specify the app from SocialApp objs (by what?)
                    twitterApp = get_object_or_404(SocialApp, name = 'twitter')
                    # to authenticate, get client_id and secret key of app and access key and secret key of account
                    accessToken = get_object_or_404(SocialToken, app = twitterApp, account = twitterAccount)
                    twitter = OAuth1Session(twitterApp.client_id, twitterApp.secret, accessToken.token, accessToken.token_secret)
                    if target.rhymer.mcname:
                        tweet = "Battle with " + target.rhymer.mcname + "'s verse:\n" + verse.tweet() + "\n#rhymeyourvibes http://rhyme.live/verses/{}".format(verse.id)
                    else:
                        tweet = "Battle with " + target.rhymer.username + "'s verse:\n" + verse.tweet() + "\n#rhymeyourvibes http://rhyme.live/verses/{}".format(verse.id)
                    params = {"status": tweet}
                    req = twitter.post("https://api.twitter.com/1.1/statuses/update.json",params = params)
                # if twitter account doesn't exist, associate it first
            notify.send(request.user, recipient = target.rhymer, verb = 'is battling with you:',  action_object=verse, target=target, description = 'beef')
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
                notify.send(user, recipient = verse.rhymer, verb = 'liked your verse:', target=verse, description = 'like')
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
                notify.send(user, recipient = verse.rhymer, verb = 'liked your verse:', target=verse, description = 'like')
                # print('liked!')
            updated = True
        data = {
            "updated": updated,
            "liked": liked,
        }
        return Response(data)
