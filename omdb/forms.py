from django import forms
from omdb.models import Video

class OmdbForm(forms.ModelForm):
    query = forms.CharField(label="Search", max_length=100)
    
    class Meta:
        model = Video
        fields = [
            'type',
        ]