from django.db import models
from django.contrib.auth.models import User
from allauth.socialaccount.models import SocialAccount
from datetime import date as datetime_date


class UserProfile(models.Model):

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE
    )
    about = models.CharField(
        max_length=150,
        blank=True
    )
    birth_date = models.DateField(
        default=datetime_date(2020, 1, 1)
    )
    avatar = models.ImageField(
        upload_to='account/avatars',
        blank=True
    )

    def __str__(self):
        return '{} - {}'.format(self.user.username, self.user.email)
    
    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'
 