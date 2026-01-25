from django.forms import ValidationError
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect, HttpResponseNotFound
from events.models import Event, Event_Tag, Tag
from django.db.models import Prefetch, Q, Count
from django.forms.models import model_to_dict
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model, authenticate, login, logout, password_validation
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.urls import reverse
from django_htmx.http import retarget, reswap
import time
from datetime import datetime
from dateutil import parser
from events.forms.events import CreateEventForm
import os
from django.contrib.auth import password_validation

# Create your views here.
def get_events_page_context():
    event_order_field_names = {
        "geolocation": "Геолокация",
        "created": "Дата",
        "title": "Наименование",
        "content": "Описание"
    }
    
    page_sizes = [ 5, 10, 25, 100]
    event_fields = [ { "id": field.name, "name": event_order_field_names[field.name] } for field in Event._meta.get_fields() if field.name in event_order_field_names]
    context = {
        "page": {
            "header": "События",
        },
        "select_options": {
            "event_order_fields": event_fields,
            "page_sizes": page_sizes,
        }
    }
    
    return context

def index(request):
    return render(request, "partials/index.html", get_events_page_context())

def events_search(request):
    order_type = request.GET.get("order_type", "asc") or "desc"
    order_by = request.GET.get("order_by", "id") or "created"
    start_date = request.GET.get("start_date", "") or ""
    end_date = request.GET.get("end_date", "") or ""
    search_text = request.GET.get("search_text", "") or ""
    page = request.GET.get("page", 1) or 1
    page_size = request.GET.get("page_size", 5) or 5
        
    if order_type == "desc":
        order_by = f"-{order_by}"

    start_date = datetime.min if start_date == "" else parser.parse(start_date)
    end_date = datetime.max if end_date == "" else parser.parse(end_date)
    
    events = (
        Event.objects
        .select_related('user_id')
        .filter(created__range=(start_date, end_date))
        .order_by(order_by)
    )

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
            "page": int(page),
            "page_size": page_size,
            "has_next": events_page.has_next(),
        }
    }
    
    if not request.htmx:
        context |= get_events_page_context()
        
        return render(request, "partials/index.html", context)
    
    return render(request, "events/search/events_search.html", context)

@login_required
def events_create(request):
    form = CreateEventForm()
    template = "events/create/post/events_create.html"
    context = {}
    
    if request.POST and request.htmx:
        form = CreateEventForm(request.POST, request.FILES)
        event = form.create_event()
        
        if event:
            event.user_id = request.user
            event.save()
            context = {
                "event": event,
                
            }
        else:
            template = "events/create/form.html"
            context = { 
                "form": form
            }
    
    response = render(request, template, context)
    
    if "event" in context:
        response["X-Entity-Created"] = "true"
        response["HX-Redirect"] = "/"
        
    return response

def accounts_create(request):
    context = {
        "page": {
            "header": "Register",
            "is_login_page": True,
        },
        "form":{
            
        }
    }
    
    errors = ""
    
    if request.method == "GET":
        return render(request, "auth/register.html", context)
    
    if request.POST:
        try:
            username = request.POST["username"]
            password = request.POST["password"]
            password2 = request.POST["password2"]
            
            try:
                password_validation.validate_password(password)
            except ValidationError as ex:
                errors += "\n ".join(ex.messages) + "\n"
            
            if User.objects.filter(username__iexact=username).exists():
                errors += "Пользователь с таким username уже существует\n"
                
            if password != password2:
                errors += "Пароли должны совпадать\n"
            
            if not errors:
                user = User.objects.create_user(username, password=password)
                login(request, user)
                return redirect("index", permanent=True)
        except Exception as ex:
            errors += "Непредвиденная ошибка при регистрации пользователя\n"    
    
    if errors:
        context['form']['errors'] = errors
        return render(request, "auth/register.html", context)
    
    return HttpResponseNotFound()
    
def accounts_login(request):
    is_login_invalid = False
    
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            # return HttpResponseRedirect(reverse('index'), headers={'HX-Redirect': reverse('index')})
            return redirect("index", permanent=True)
        else:
            is_login_invalid = True
            
    context = {
        "page": {
            "header": "Log In",
            "is_login_page": True,
        },
        "form":{
            "is_login_invalid": is_login_invalid
        }
    }
    
    return render(request, "auth/login.html", context)

@login_required
def accounts_logout(request):
    logout(request)
    
    context = {}
    
    return redirect("accounts_login")