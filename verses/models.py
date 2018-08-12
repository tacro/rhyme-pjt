from django.db import models
from users.models import User

class Verse(models.Model):
    """each post of Rhyme.live"""
    rhymer = models.ForeignKey(User, on_delete = models.CASCADE)
    pub_date = models.DateTimeField(auto_now = True)
    body = models.TextField(max_length = 500)
    likes = models.ManyToManyField(User, blank=True, related_name = 'verse_likes')

    def __str__(self):
        return self.body[:15]

    def get_absolute_url(self):
        return "/verses/%i" % self.id

    def get_like_url(self):
        return "/verses/%i/like" % self.id

    def get_api_like_url(self):
        return "/verses/api/%i/like" % self.id
