from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.db import models
# Create your models here.

User = settings.AUTH_USER_MODEL # "auth.User"


class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    value = models.CharField(null=True, blank=True)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey("content_type", "object_id")