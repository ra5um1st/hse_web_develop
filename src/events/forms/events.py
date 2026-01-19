# from django import forms
from events.models import Event
from django.contrib.gis import forms

class CreateEventForm(forms.Form):
    # class Meta:
    #     model = Event
    #     fields = ['title', 'geolocation']
    
    title = forms.CharField()
    content = forms.CharField(
        widget=forms.Textarea())
    geolocation = forms.PointField(widget=forms.OSMWidget(
                  attrs={
                         'map_width': 600,
                         'map_height': 400,
                         'default_lat': 50.1091,
                         'default_lon': 8.6819,
                         'default_zoom': 9,
                         'class': 'h-100 w-100'
                        }))
    # tags = forms.ModelMultipleChoiceField(
    #     Tag.objects.values_list("name", flat=True), 
    #     required=False)
    created = forms.DateTimeField(required=False)
    
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
                geolocation = self.cleaned_data["geolocation"]
                created = self.cleaned_data["created"]
                media = self.cleaned_data["media"] 
        
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
            except:
                self.add_error(None, 'Не удалось создать событие')
                return None
    