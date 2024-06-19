from django_filters import FilterSet, CharFilter, ModelChoiceFilter, DateTimeFilter, ChoiceFilter
from django.forms import DateTimeInput
from .models import Category
from .resources import CATEGORY_TYPE


class PostFilter(FilterSet):
    name = CharFilter(
        field_name='content_title',
        lookup_expr='icontains',
        label='Название'
    )

    post_type = ChoiceFilter(
        field_name='content_category',
        choices=CATEGORY_TYPE,
        label='Тип поста'
    )

    category = ModelChoiceFilter(
        field_name='post_category',
        queryset=Category.objects.all(),
        label='Категория',
        empty_label='Все категории',
    )

    added_after = DateTimeFilter(
        field_name='date_create',
        lookup_expr='gt',
        label='Дата публикации начиная с',
        widget=DateTimeInput(
            format='%Y-%m-%dT%H:%M',
            attrs={'type': 'datetime-local'},
        ),
    )
