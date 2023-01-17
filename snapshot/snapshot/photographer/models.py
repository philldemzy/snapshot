import uuid

from django.db import models


def profile_upload(instance, filename):
    return f'profile/{instance.id}/{filename}'


def media_upload(instance, filename):
    return f'media/{instance.photographer.id}/{str(uuid.uuid4()) + filename(".")[-1]}'


# Create your models here.
class Photographer(models.Model):
    first_name = models.CharField(max_length=55)
    last_name = models.CharField(max_length=55)
    bio = models.CharField(max_length=200)
    profile = models.ImageField(upload_to=profile_upload)
    brand_name = models.CharField(max_length=100)
    country = models.CharField(max_length=60)
    state = models.CharField(max_length=60)
    city = models.CharField(max_length=60)
    other_addy = models.CharField(max_length=150)


class Media(models.Model):
    photographer = models.ForeignKey(Photographer, on_delete=models.CASCADE, related_name='uploaded_media')
    upload = models.FileField(upload_to=media_upload)
