from __future__ import unicode_literals
from django.core.urlresolvers import reverse
from django.db import models

# Create your models here.


class Site(models.Model):
    site_title = models.CharField(max_length=250)
    site_url = models.CharField(max_length=1000)
    def get_absolute_url(self):
        return reverse('repo:detail', kwargs={'pk': self.pk})

    def __str__(self):
        return self.site_title + " - " + self.site_url


class Url(models.Model):
    site = models.ForeignKey(Site, on_delete=models.CASCADE)
    url_title = models.CharField(max_length=1000)
    url = models.CharField(max_length=250)

    def __str__(self):
        return str(self.site_id) + " " +  self.url_title + ": " + self.url

    def get_absolute_url(self):
        return reverse('repo:detail', kwargs={'pk': self.site_id})
