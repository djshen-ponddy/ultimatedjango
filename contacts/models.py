from django.contrib.auth.models import User
from django.db import models
from shortuuidfield import ShortUUIDField

from accounts.models import Account


# Create your models here.


class Contact(models.Model):
    uuid = ShortUUIDField(unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    role = models.CharField(max_length=20)
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    account = models.ForeignKey(Account)
    owner = models.ForeignKey(User)
    created_on = models.DateField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'contacts'

    @property
    def full_name(self):
        return '%s %s' % (self.first_name, self.last_name)

    def __str__(self):
        return '%s' % self.full_name

    @models.permalink
    def get_absolute_url(self):
        return 'contacts:detail', [self.uuid]

    @models.permalink
    def get_update_url(self):
        return 'contacts:update', [self.uuid]

    @models.permalink
    def get_delete_url(self):
        return 'contacts:delete', [self.uuid]
