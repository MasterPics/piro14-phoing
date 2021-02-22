from .models import Location
from myApp.models import Place
from django import forms


class LocationForm(forms.ModelForm):
    class Meta:
        model = Location
        fields = ('address', 'lat', 'lon',)
        # exclude = ('start_date_time', 'end_date_time',)
        widgets = {
            'address': forms.TextInput(
                attrs={'class': 'form-control location location-address',
                       'id': 'location-address',
                       'style': 'width:100%; margin:0 auto;',
                       'placeholder': ''}
            ),
            'lat': forms.TextInput(
                attrs={'class': 'form-control location location-lat',
                       'id': 'location-lat',
                       'style': 'width:30%;'}
            ),
            'lon': forms.TextInput(
                attrs={'class': 'form-control location location-lon',
                       'id': 'location-lon',
                       'style': 'width:30%;'}
            ),
        }
        labels = {
            'address': '도로명 주소',
            'lat': 'latitude',
            'lon': 'longitude',
        }
        required = {
            # 'address':True,
            # 'lat':True,
            # 'lon':True,
        }


class PlaceForm(forms.ModelForm):

    class Meta:
        model = Place
        fields = ('thumbnail', 'title', 'desc', 'pay', 'tag_str')
        # exclude = ('start_date_time', 'end_date_time',)
        widgets = {
            # 'thumbnail': forms.ImageField(
            #     attrs={
            #         'class': 'form-control place place-thumbnail',
            #         'id': 'place-thumbnail',
            #     }
            # ),
            'title': forms.TextInput(
                attrs={
                    'class': 'form-control place place-title',
                    'id': 'place-title',
                    'placeholder': ''
                }
            ),
            'desc': forms.Textarea(
                attrs={'class': 'form-control place place-desc',
                       'id': 'place-desc',
                       }
            ),
            # 'pay': forms.IntegerField(
            #     attrs={
            #         'class': 'form-control place place-pay',
            #         'id': 'place-pay',
            #     }
            # ),
            'tag_str': forms.TextInput(
                attrs={
                    'class': 'form-control place place-tag-str',
                    'id': 'place-tag-str',
                }
            ),
        }
        labels = {
            'thumbnail': 'Thumbnail',
            'title': 'Title',
            'desc': 'Description',
            'pay': 'Payment',
            'tag_str': 'Hashtag',
        }

        required = {
            'thumbnail': True,
            'title': True,
            'desc': True,
            'pay': True,
        }
