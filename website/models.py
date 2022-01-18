from django.db import models


class Photo(models.Model):

    filename = models.CharField(max_length=264, unique=True)
    url = models.URLField(unique=True)
    url_small = models.URLField(unique=True)
    category = models.CharField(max_length=64)
    description = models.CharField(max_length=264)
    orientation = models.CharField(max_length=64)
