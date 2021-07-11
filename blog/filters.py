from django_filters import FilterSet, ModelMultipleChoiceFilter
from taggit.models import Tag

from blog.models import Post


class PostFilter(FilterSet):
    tag = ModelMultipleChoiceFilter(conjoined=True,
                                    field_name="tags__name",
                                    to_field_name="name",
                                    queryset=Tag.objects.all())

    class Meta:
        model = Post
        fields = {
            'title': ['contains'],
            'description': ['contains'],
            'author': ['exact'],
            'timestamp_created': ['date__gte', 'date__lte'],
            # 'tags__name': ['exact']
        }
