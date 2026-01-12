from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from events.models import Event, Event_Tag, Tag
from django.db.models import Prefetch, Q, Count
from django.forms.models import model_to_dict
from django.core.paginator import Paginator
import time
from datetime import datetime
from dateutil import parser

# Create your views here.
def index(request):
    event_order_field_names = {
        "geolocation": "Геолокация",
        "created": "Дата",
        "title": "Наименование",
        "content": "Описание"
    }
    page_sizes = [ 5, 10, 25, 100]
    event_fields = [ { "id": field.name, "name": event_order_field_names[field.name] } for field in Event._meta.get_fields() if field.name in event_order_field_names]

    time.sleep(1)
    order_type = request.GET.get("order_type", "asc")
    order_by = request.GET.get("order_by", event_fields[0]["id"])
    start_date = request.GET.get("start_date", "")
    end_date = request.GET.get("end_date", "")
    search_text = request.GET.get("search_text", "")
    page = request.GET.get("page", 1)
    page_size = request.GET.get("page_size", 5)

    if order_type == "desc":
        order_by = f"-{order_by}"

    start_date = datetime.min if start_date == "" else parser.parse(start_date)
    end_date = datetime.max if end_date == "" else parser.parse(end_date)

    events = Event.objects.filter(created__range=(start_date, end_date)).order_by(order_by)

    if search_text:
        words = search_text.split()
        q = Q(
            Q(title__istartswith=words[0]) |
            Q(content__istartswith=words[0])
        )

        for word in words[1:]:
            q |= Q(
                Q(title__istartswith=word) |
                Q(content__istartswith=word)
            )

        events = events.filter(q)

    events_paginator = Paginator(events, page_size)
    events_page = events_paginator.page(page)
    popular_tags = Tag.objects.filter(
        event__in=events
        ).annotate(
            count=Count('event')
        ).order_by('-count')[:3]

    context = {
        "events": events_page.object_list,
        "select_options": {
            "event_order_fields": event_fields,
            "page_sizes": page_sizes,
        },
        "stats": {
            "events_count": events_paginator.count,
            "popular_tags": popular_tags,
        },
        "form": {
            "order_type": order_type,
            "order_by": order_by.strip('-'),
            "start_date": start_date.isoformat() if start_date != datetime.min else "",
            "end_date": end_date.isoformat()  if end_date != datetime.max else "",
            "search_text": search_text,
            "page": int(page) + 1,
            "page_size": page_size,
            "has_next": events_page.has_next(),
        }
    }

    template = "index.html"

    if request.htmx:
        template = "partials/filter_events.html"

    return render(request, template, context)