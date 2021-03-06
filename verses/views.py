from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.generic import RedirectView
from .models import Verse
from beats.models import Beat
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
# twitter card
from PIL import Image, ImageDraw, ImageFont
import textwrap, io, uuid
from django.core.files.base import ContentFile

@login_required
def create(request):
    if request.method == 'POST':
        if request.POST['body']:
            verse = Verse()
            verse.body = request.POST['body']
            verse.rhymer = request.user
            if request.POST['beats-list'] == 'no-beat' or request.POST['beats-list'] =='default':
                verse.beat = None
            else:
                beat = get_object_or_404(Beat, id = request.POST['beats-list'])
                verse.beat = beat
            # make a verse's image for twitter card
            font_size = 100
            font_name = "static/verses/fonts/Yu_Gothic_Medium.otf"
            img_io = io.BytesIO()
            img = Image.open("static/verses/img/verse_bg.png")
            draw = ImageDraw.Draw(img)
            font = ImageFont.truetype(font_name, font_size)
            text_origin = request.POST['body']
            text = textwrap.fill(text_origin, 20, max_lines = 4, placeholder='...')
            draw.multiline_text((235, 380), text, fill ='#FFCF35', font = font, spacing = 35, align = 'left')
            # img.save()
            img.save(img_io, format='PNG')
            img_file = ContentFile(img_io.getvalue(), '{}.jpg'.format(uuid.uuid4()))
            verse.image = img_file
            verse.save()
            url_ = 'home'
            # if user chose to share post on twitter
            if request.POST.get('tweetBtn', False):
                # specify the uesr's twitter account
                try:
                    twitterAccount = SocialAccount.objects.get(user = request.user, provider = 'twitter')
                    twitterApp = get_object_or_404(SocialApp, name = 'twitter')
                    accessToken = get_object_or_404(SocialToken, app = twitterApp, account = twitterAccount)
                    twitter = OAuth1Session(twitterApp.client_id, twitterApp.secret, accessToken.token, accessToken.token_secret)
                    if verse.rhymer.mcname:
                        tweet = verse.rhymer.mcname + " が1バースKickしました！\n#rhymeyourvibes\nhttps://rhyme.live/verses/{}".format(verse.id)
                    else:
                        tweet = verse.rhymer.username + " が1バースKickしました！\n#rhymeyourvibes\nhttps://rhyme.live/verses/{}".format(verse.id)
                    params = {"status": tweet}
                    req = twitter.post("https://api.twitter.com/1.1/statuses/update.json",params = params)
                # if twitterAccount doesn't exist, associate it first.
                except SocialAccount.DoesNotExist:
                    url_ ='/accounts/social/connections/'
            return redirect(url_)
        else:
            beats = Beat.objects
            return render(request, 'verses/create.html', {'error': 'Please enter your verse', 'beats':beats})
    else:
        beats = Beat.objects
        return render(request, 'verses/create.html', {'beats':beats})

@login_required
def delete(request, verse_id):
    verse = get_object_or_404(Verse, pk = verse_id)
    if verse.rhymer == request.user:
        if verse.image and verse.image != '/static/rhyme/img/rhymer_live.jpg':
            verse.image.delete()
        verse.delete()
        return redirect('home')
    else:
        return redirect('home', {'error': 'You are not allowed to delete this'})

def index(request):
    verses_list = Verse.objects.order_by('-pub_date')
    page = request.GET.get('page',1)
    paginator = Paginator(verses_list, 15)
    try:
        verses = paginator.page(page)
    except PageNotAnInteger:
        verses = paginator.page(1)
    except EmptyPage:
        verses = paginator.page(paginator.num_pages)
    return render(request, 'verses/index.html', {'verses':verses})

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
            verse.beat = target.beat
            # make a verse's image for twitter card
            font_size = 100
            font_name = "static/verses/fonts/Yu_Gothic_Medium.otf"
            img_io = io.BytesIO()
            img = Image.open("static/verses/img/verse_bg.png")
            draw = ImageDraw.Draw(img)
            font = ImageFont.truetype(font_name, font_size)
            text_origin = request.POST['body']
            text = textwrap.fill(text_origin, 20, max_lines = 4, placeholder='...')
            draw.multiline_text((235, 380), text, fill ='#FFCF35', font = font, spacing = 35, align = 'left')
            # img.save()
            img.save(img_io, format='PNG')
            img_file = ContentFile(img_io.getvalue(), '{}.jpg'.format(uuid.uuid4()))
            verse.image = img_file
            verse.save()
            url_ = 'home'
            if request.POST.get('tweetBtn', False):
                # specify the uesr's twitter account
                try:
                    twitterAccount = SocialAccount.objects.get(user = request.user, provider = 'twitter')
                    twitterApp = get_object_or_404(SocialApp, name = 'twitter')
                    accessToken = get_object_or_404(SocialToken, app = twitterApp, account = twitterAccount)
                    twitter = OAuth1Session(twitterApp.client_id, twitterApp.secret, accessToken.token, accessToken.token_secret)
                    if target.rhymer.mcname:
                        tweet = target.rhymer.mcname + "のバースにアンサーしました！\n#rhymeyourvibes\nhttps://rhyme.live/verses/{}".format(verse.id)
                    else:
                        tweet = target.rhymer.username + "のバースにアンサーしました！\n#rhymeyourvibes\nhttps://rhyme.live/verses/{}".format(verse.id)
                    params = {"status": tweet}
                    req = twitter.post("https://api.twitter.com/1.1/statuses/update.json",params = params)
                # if twitterAccount doesn't exist, associate it first.
                except SocialAccount.DoesNotExist:
                    url_ ='/accounts/social/connections/'
            notify.send(request.user, recipient = target.rhymer, verb = ' answered to you:', action_object=verse, target=target, description = 'answer')
            return redirect(url_)
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
            verse.beat = target.beat
            # make a verse's image for twitter card
            font_size = 100
            font_name = "static/verses/fonts/Yu_Gothic_Medium.otf"
            img_io = io.BytesIO()
            img = Image.open("static/verses/img/verse_bg.png")
            draw = ImageDraw.Draw(img)
            font = ImageFont.truetype(font_name, font_size)
            text_origin = request.POST['body']
            text = textwrap.fill(text_origin, 20, max_lines = 4, placeholder='...')
            draw.multiline_text((235, 380), text, fill ='#FFCF35', font = font, spacing = 35, align = 'left')
            # img.save()
            img.save(img_io, format='PNG')
            img_file = ContentFile(img_io.getvalue(), '{}.jpg'.format(uuid.uuid4()))
            verse.image = img_file
            verse.save()
            url_ = 'home'
            if request.POST.get('tweetBtn', False):
                # specify the uesr's twitter account
                try:
                    twitterAccount = SocialAccount.objects.get(user = request.user, provider = 'twitter')
                    twitterApp = get_object_or_404(SocialApp, name = 'twitter')
                    accessToken = get_object_or_404(SocialToken, app = twitterApp, account = twitterAccount)
                    twitter = OAuth1Session(twitterApp.client_id, twitterApp.secret, accessToken.token, accessToken.token_secret)
                    if target.rhymer.mcname:
                        if verse.rhymer.mcname:
                            tweet = verse.rhymer.mcname + "が" + target.rhymer.mcname + "とラップバトル中！\n#rhymeyourvibes\nhttps://rhyme.live/verses/{}".format(verse.id)
                        else:
                            tweet = verse.rhymer.username + "が" + target.rhymer.mcname + "とラップバトル中！\n#rhymeyourvibes\nhttps://rhyme.live/verses/{}".format(verse.id)
                    else:
                        if verse.rhymer.mcname:
                            tweet = verse.rhymer.mcname + "が" + target.rhymer.username + "とラップバトル中！\n#rhymeyourvibes\nhttps://rhyme.live/verses/{}".format(verse.id)
                        else:
                            tweet = verse.rhymer.username + "が" + target.rhymer.username + "とラップバトル中！\n#rhymeyourvibes\nhttps://rhyme.live/verses/{}".format(verse.id)
                    params = {"status": tweet}
                    req = twitter.post("https://api.twitter.com/1.1/statuses/update.json",params = params)
                # if twitterAccount doesn't exist, associate it first.
                except SocialAccount.DoesNotExist:
                    url_ ='/accounts/social/connections/'
            notify.send(request.user, recipient = target.rhymer, verb = 'is battling with you:',  action_object=verse, target=target, description = 'beef')
            return redirect(url_)
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
