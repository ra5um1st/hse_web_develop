# from django import forms
from events.models import Event
from django import forms
from django.contrib.gis.geos import Point
# from django.contrib.gis import forms

class CreateEventForm(forms.Form):
    # class Meta:
    #     model = Event
    #     fields = ['title', 'geolocation']
    title = forms.CharField()
    content = forms.CharField(widget=forms.Textarea())
    geolocation_lng = forms.FloatField()
    geolocation_lat = forms.FloatField()
    created = forms.DateTimeField(required=False)
    # tags = forms.ModelMultipleChoiceField(
    #     Tag.objects.values_list("name", flat=True), 
    #     required=False)
    
    # def clead_media(self):
    #     max_size = 65536
    #     media = self.cleaned_data["media"]
    #     if media._size > max_size:
    #         raise forms.ValidationError(f"Файл должен быть не более {max_size} байт")
    
    def save(self):        
        if self.is_valid():
            try:
                title = self.cleaned_data["title"]
                content = self.cleaned_data["content"]
                geolocation_lng = self.cleaned_data["geolocation_lng"]
                geolocation_lat = self.cleaned_data["geolocation_lat"]
                geolocation = Point(geolocation_lng, geolocation_lat, srid=4326)
                created = self.cleaned_data["created"]
                media = self.cleaned_data.get("media", None) 
        
                media_bytes = []
                if media:
                    # path, extension = os.path.splitext(media)
                    with open("in-file", "rb") as file:
                        media_bytes = file.read() 
                        
                event = Event(
                    title=title,
                    content=content, 
                    created=created,
                    geolocation=geolocation,
                    media_type=None if not media else "gif" if media.endswith("gif") else "image",
                    media_bytes=None if not media else media_bytes)
                
                return event
            except Exception as e:
                self.add_error(None, 'Не удалось создать событие')
                return None
    