from django.contrib.auth.models import User
from django.db import models


class UserProfile(models.Model):
    user = models.OneToOneField(User, primary_key=True, verbose_name='user', related_name='profile')
    avatar = models.TextField()
    has_notification = models.BooleanField(default=False)

    def __unicode__(self):
        return "{}'s profile".format(self.user.username)

    class Meta:
        db_table = 'user_profile'


class Notification(models.Model):
    user = models.ForeignKey(User, related_name='notifications')
    date = models.DateTimeField(auto_now=True, blank=False, null=False, db_index=True)
    detail = models.TextField(blank=False, null=False)
    read = models.BooleanField(default=False)
    deleted = models.BooleanField(default=False)

    class Meta():
        ordering = ['-date']
