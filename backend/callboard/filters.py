from django_filters import FilterSet, DateFilter
from django import forms
from .models import Advert, Category

class AdvertFilters(FilterSet):
    category = forms.ModelMultipleChoiceField(
        queryset=Category.objects.all(),
        widget=forms.CheckboxSelectMultiple
    )
    created = DateFilter(
        field_name='created',
        lookup_expr='gt',
        widget=forms.DateInput(attrs={'type': 'date'}),
        label='Дата'
    )

    class Meta:
        model = Advert
        fields = {
            'subject': ['icontains'],
            'created': ['gt'],
            'category': ['exact'],
            'price': ['lt', 'gt'],
        }

class AdvertFiltrForm(forms.ModelForm):
    filterset = AdvertFilters()

    class Meta:
        model = Advert
        fields = [
            'category',
            'subject',
            'date',
        ]