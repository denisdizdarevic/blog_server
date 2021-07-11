from django_filters import FilterSet

from blog.models import Post


class PostFilter(FilterSet):
    class Meta:
        model = Post
        fields = {
            'title': ['contains'],
            'description': ['contains'],
            'author': ['exact'],
            'timestamp_created': ['date__gte', 'date__lte'],
            'tags__name': ['exact', 'in']
        }