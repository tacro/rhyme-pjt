from django.db import models
from users.models import User

class Beat(models.Model):
    """
    track for verses
    """
    maker = models.ForeignKey(User, on_delete = models.CASCADE)
    pub_date = models.DateTimeField(auto_now = True)
    track = models.FileField(upload_to = 'music/beats')
    title = models.CharField(max_length = 50,
                             unique = False,)
    image = models.ImageField(upload_to = 'images/beats', default = '/static/beats/img/vinyl.png')

    def __str__(self):
        return self.title[:20]
