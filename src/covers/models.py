from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.db import models
from django.db.models import Avg
from django.db.models.signals import post_save

User = settings.AUTH_USER_MODEL # "auth.User"


class Cover(models.Model):
    field_name = models.ImageField(upload_to=None, height_field=None, width_field=None, max_length=100,default="../static/images/mounting.jpg")
    object_id = models.PositiveIntegerField()

