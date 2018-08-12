from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.generic import RedirectView
from .models import Verse

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

class PostLikeRedirect(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        # slug = self.kwargs.get("slug")
        # print(slug)
        verse = get_object_or_404(Verse, pk=verse_id)
        return verse.get_absolute_url()
