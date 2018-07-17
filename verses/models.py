from django.db import models
from django.contrib.auth.models import User

class Verse(models.Model):
    """each post of Rhyme.live"""
    rhymer = models.ForeignKey(User, on_delete = models.CASCADE)
    pub_date = models.DateTimeField(auto_now = True)
    body = models.TextField(max_length = 500)
