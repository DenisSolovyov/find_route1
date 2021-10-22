from django import forms
from cities.models import City


class HtmlForm(forms.Form):
    name = forms.CharField(label='Город')


class RouteForm(forms.Form):
    from_city = forms.ModelChoiceField(label='Откуда', queryset=City.objects.all(),
                                       widget=forms.Select(attrs={"class": 'form-control js-example-basic-single'}))

    to_city = forms.ModelChoiceField(label='Куда', queryset=City.objects.all(),
                                     widget=forms.Select(attrs={"class": 'form-control js-example-basic-single'}))

    traveling = forms.IntegerField(label='Время в пути',
                                   widget=forms.NumberInput(attrs=
                                                            {"class": 'form-control',
                                                             'placeholder': 'Время в пути'}))
    cities = forms.ModelMultipleChoiceField(
        label='Через города', queryset=City.objects.all(),
        required=False,
        widget=forms.SelectMultiple(attrs={"class": 'form-control js-example-basic-multiple'}))

    name = forms.CharField(label='Номер поезда', widget=forms.TextInput(
        attrs={"class": 'form-control', 'placeholder': 'Введите номер поезда'}))

    # class Meta:
    #     model = Train
    #     fields = ['name', 'from_city', 'to_city', 'travel_time']
