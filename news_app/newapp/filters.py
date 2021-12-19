from django_filters import FilterSet, DateFromToRangeFilter
from .models import Post


class NewsFilter(FilterSet):
    dateCreation = DateFromToRangeFilter()

    class Meta:
        model = Post
        fields = ('author', 'category', 'dateCreation')
