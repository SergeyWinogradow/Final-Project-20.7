
from django.core.exceptions import ValidationError
from django_filters import FilterSet, DateFilter
from .models import Category, Advert
from django import forms
from .filters import AdvertFilters


class AdvertForm(forms.ModelForm):
   class Meta:
       model = Advert
       fields = [
           'user',
           'category',
           'filters',
           'date',
           'subject',
           'description',
           'images',
           'price',
           'moderation',
           'slug',
       ]

       def create(self, request):
           request["user"] = self.context['request'].user
           advert = Advert.objects.create(**request)
           return advert

       def clean(self):
            cleaned_data = super().clean()
            name = cleaned_data.get("subject")
            description = cleaned_data.get("description")

            if name == description:
                raise ValidationError(
                    "Описание не должно быть идентично названию."
                )

            return cleaned_data



class AdvertFiltrForm(FilterSet):
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



