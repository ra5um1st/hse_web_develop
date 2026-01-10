from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from events.models import Event, Event_Tag
from django.db.models import Prefetch
from django.forms.models import model_to_dict

# Create your views here.
def index(request):
    events_with_tags = Event.objects.all()
    event_field_names = {
        "location": "Геолокация",
        "created": "Дата",
        "title": "Наименование",
        "content": "Описание"
    }
    event_fields = [ { "id": field.name, "name": event_field_names[field.name] } for field in Event._meta.get_fields() if field.name in event_field_names]
    # print(event_fields)

    context = {
        "events": events_with_tags,
        "event_fields": event_fields,
    }

    return render(request, "index.html", context)