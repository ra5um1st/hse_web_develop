from django.shortcuts import render
from django.http import HttpResponse
from events.models import Event

# Create your views here.
def index(request):
    context = {
        "events": list(Event.objects.all()) * 1
    }
    return render(request, "index.html", context)