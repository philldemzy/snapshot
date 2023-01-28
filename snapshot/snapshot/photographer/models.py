import uuid

from django.db import models


def profile_upload(instance, filename):
    return f'profile/{instance.id}/{filename}'


def media_upload(instance, filename):
    return f'media/{instance.photographer.id}/{str(uuid.uuid4()) + filename.split(".")[-1]}'


# Create your models here.
class Photographer(models.Model):
    first_name = models.CharField(max_length=55)
    last_name = models.CharField(max_length=55)
    bio = models.CharField(max_length=200)
    password = models.CharField(max_length=150)
    email = models.EmailField(unique=True)
    phone_num = models.CharField(unique=True, max_length=20)
    profile = models.ImageField(upload_to=profile_upload)
    brand_name = models.CharField(max_length=100, unique=True)
    country = models.CharField(max_length=60)
    state = models.CharField(max_length=60)
    city = models.CharField(max_length=60)
    other_addy = models.CharField(max_length=150)
    min_price = models.DecimalField(max_digits=15, decimal_places=10)
    max_price = models.DecimalField(max_digits=15, decimal_places=10)

    def is_price_range(self, bid):
        return self.min_price <= bid <= self.max_price


class Media(models.Model):
    photographer = models.ForeignKey(Photographer, on_delete=models.CASCADE, related_name='uploaded_media')
    upload = models.FileField(upload_to=media_upload)
    alt = models.CharField(max_length=60, null=True, blank=True)
