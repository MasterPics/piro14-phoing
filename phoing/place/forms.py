from myApp.models import Contact
from django import forms


class PlaceForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ('location', 'lat', 'lon',)
        # exclude = ('start_date_time', 'end_date_time',)
        widgets = {
            'location': forms.TextInput(
                attrs={'class': 'form-control place place-location',
                       'id': 'place-location',
                       'style': 'width:100%; margin:0 auto;',
                       'placeholder': ''}
            ),
            'lat': forms.TextInput(
                attrs={'class': 'form-control place place-lat',
                       'id': 'place-lat',
                       'style': 'width:30%;'}
            ),
            'lon': forms.TextInput(
                attrs={'class': 'form-control place place-lon',
                       'id': 'place-lon',
                       'style': 'width:30%;'}
            ),
        }
        labels = {
            'location': '도로명 주소',
            'lat': 'latitude',
            'lon': 'longitude',
        }
        required = {
            # 'location':True,
            # 'lat':True,
            # 'lon':True,
        }
