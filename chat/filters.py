from django import forms
import django_filters
from django_filters import CharFilter
from .models import Room, Category


class RoomFilter(django_filters.FilterSet):
    name = CharFilter(field_name="name", lookup_expr="icontains", label="Sala")
    description = CharFilter(field_name="description", lookup_expr="icontains", label="Descrição")
    category = django_filters.ModelChoiceFilter(
        field_name="category",
        queryset=Category.objects.all(),
        widget=forms.Select,
        label="Categoria",
    )

    class Meta:
        model = Room
        fields = ["name", "description", "category"]
