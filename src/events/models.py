from django.contrib.gis.db import models
from datetime import datetime
from django.contrib.auth import get_user_model
import json
from django.forms.models import model_to_dict

# Create your models here.
class Tag(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=127)
    
    def __str__(self):
        return json.dumps(model_to_dict(self), indent=4, ensure_ascii=False)

class Event(models.Model):
    id = models.BigAutoField(primary_key=True)
    user_id = models.ForeignKey(get_user_model(), on_delete=models.SET_DEFAULT, default=None)
    geolocation = models.PointField(spatial_index=True)
    created = models.DateTimeField(default=datetime.now())
    updated = models.DateTimeField(blank=True, null=True)
    title = models.CharField(max_length=127)
    content = models.CharField(max_length=4095)
    media_type = models.CharField(max_length=15, blank=True, null=True)
    media_url = models.CharField(max_length=2047, blank=True, null=True)
    
    tags = models.ManyToManyField(Tag, through='Event_Tag')
    
    def __str__(self):
        return json.dumps(self.title, indent=4, ensure_ascii=False)

class Event_Tag(models.Model):
    id = models.BigAutoField(primary_key=True)
    event_id = models.ForeignKey(Event, on_delete=models.CASCADE)
    tag_id = models.ForeignKey(Tag, on_delete=models.CASCADE)

    def __str__(self):
        return json.dumps(model_to_dict(self), indent=4, ensure_ascii=False)
