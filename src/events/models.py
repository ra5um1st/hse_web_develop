from django.contrib.gis.db import models
from datetime import datetime
from django.contrib.auth import get_user_model

# Create your models here.
class Event(models.Model):
    id = models.BigAutoField(primary_key=True)
    user_id = models.ForeignKey(get_user_model(), on_delete=models.SET_DEFAULT, default=None)
    location = models.PointField(null=False, spatial_index=True)
    created = models.DateTimeField(null=False, default=datetime.now())
    updated = models.DateTimeField(null=True)
    title = models.CharField(max_length=127, null=False)
    content = models.CharField(max_length=4095, null=False)
    media_type = models.CharField(max_length=15)
    media_url = models.CharField(max_length=2047)

class Tag(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=127)
    
class Event_Tag(models.Model):
    id = models.BigAutoField(primary_key=True)
    event_id = models.ForeignKey(Event, on_delete=models.CASCADE)
    tag_id = models.ForeignKey(Tag, on_delete=models.CASCADE)
