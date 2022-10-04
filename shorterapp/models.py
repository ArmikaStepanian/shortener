from django.db import models


class Link(models.Model):
    shortlink = models.CharField(max_length=255)
    longlink = models.TextField(blank=False)
