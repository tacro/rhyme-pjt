from django.db import models
from users.models import User

class Verse(models.Model):
    """
    each post of Rhyme.live
    target : set target when the obj is a reply to another.
    type : identifies what type it is out of these 3 kinds;
            0: normal
            1: answer
            2: beef
    """
    rhymer = models.ForeignKey(User, on_delete = models.CASCADE)
    pub_date = models.DateTimeField(auto_now = True)
    body = models.TextField(max_length = 500)
    likes = models.ManyToManyField(User,
                                   blank=True,
                                   related_name = 'verse_likes')
    target = models.ForeignKey('Verse',
                               on_delete = models.SET_NULL,
                               blank = True,
                               null = True)
    type = models.IntegerField(default = 0)

    def __str__(self):
        return self.body[:15]

    def get_absolute_url(self):
        return "/verses/%i" % self.id

    def get_like_url(self):
        return "/verses/%i/like" % self.id

    def get_api_like_url(self):
        url_ = '/verses/api/%i/like' % self.id
        print(url_)
        return url_
