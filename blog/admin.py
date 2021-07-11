from django.contrib import admin
from django.forms import ModelForm
from django.forms.widgets import TextInput, SelectMultiple
from django_summernote.widgets import SummernoteWidget
from taggit.forms import TagField
from taggit_labels.widgets import LabelWidget

from blog.models import Post


class PostAdminForm(ModelForm):
    tags = TagField(required=False, widget=LabelWidget)
    class Meta:
        model = Post
        fields = '__all__'
        widgets = {
            'title': TextInput,
            'description': SummernoteWidget,
            'content': SummernoteWidget
        }


class PostAdmin(admin.ModelAdmin):
    form = PostAdminForm

    def get_queryset(self, request):
        query = super().get_queryset(request)
        if request.user.is_superuser:
            return query
        else:
            return query.filter(author=request.user)

    def save_model(self, request, obj, form, change):
        if obj.author is None:
            obj.author = request.user
        super().save_model(request, obj, form, change)

    def get_changeform_initial_data(self, request):
        return {'author': request.user}

    def get_fields(self, request, obj=None):
        fields = super().get_fields(request, obj)

        if obj is None and not request.user.is_superuser:
            fields.remove('author')

        return fields

    def get_readonly_fields(self, request, obj=None):
        if not request.user.is_superuser and obj is not None:
            if obj.author == request.user:
                return ['author']
            else:
                return ['title', 'description', 'content', 'author']
        return []


admin.site.register(Post, PostAdmin)