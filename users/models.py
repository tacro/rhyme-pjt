from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, UserManager
from django.contrib.auth.validators import ASCIIUsernameValidator
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from django.core.mail import send_mail

class User(AbstractBaseUser, PermissionsMixin):
    #username
    username_validator = ASCIIUsernameValidator()
    username = models.CharField(
        _('username'),
        max_length = 50,
        unique = True,
        help_text=_('Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'),
        validators=[username_validator],
        error_messages={
            'unique': _("A user with that username already exists."),
        },
    )
    #mcname
    mcname = models.CharField(
        _('MC name'),
        max_length = 50,
        unique = False,
        blank = True,
    )
    #Email
    email = models.EmailField(_('email address'))
    icon = models.ImageField(_('icon'), upload_to = 'images/icons', null=True, blank=True)
    biography = models.CharField(max_length = 150, blank=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_('Designates whether the user can log into this admin site.'),
    )
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    objects = UserManager()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email',]

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
        db_table = 'users'

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def email_user(self, subject, message, from_email=None, **kwargs):
        send_mail(subject, message, from_email, [self.email], **kwargs)

    def get_follows(self):
        relations = Relationship.objects.filter(follower=self)
        return [relation.follow for relation in relations]

    def get_followers(self):
        relations = Relationship.objects.filter(follow=self)
        return [relation.follower for relation in relations]

"""
    def get_index_url(self):
        return "/verses/index/{}".format(self.id)
"""


'''
medium table to connect follow/follower
'''
class Relationship(models.Model):
    follow = models.ForeignKey(User,
        on_delete = models.CASCADE,
        related_name = 'follows')
    follower = models.ForeignKey(User,
        on_delete = models.CASCADE,
        related_name = 'followers')
