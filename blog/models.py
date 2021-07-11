from django.db import models
from django.contrib.auth import get_user_model
from taggit.managers import TaggableManager


class Post(models.Model):
    title = models.TextField()
    description = models.TextField()
    content = models.TextField()
    author = models.ForeignKey(get_user_model(), null=True, on_delete=models.SET_NULL)
    timestamp_created = models.DateTimeField(auto_now_add=True)
    timestamp_edited = models.DateTimeField(auto_now=True)
    tags = TaggableManager()

    def __str__(self):
        return f'{self.id}: {self.title}'

    def get_like(self, user):
        return self.likes.filter(author__exact=user)

    def set_like(self, user, like):
        like_query = self.get_like(user)
        if like == False and like_query.exists():
            like_query.delete()
        elif like == True and not like_query.exists():
            Like.objects.create(author=user, post=self).save()


class Comment(models.Model):
    content = models.TextField()
    author = models.ForeignKey(get_user_model(), null=True, on_delete=models.SET_NULL)
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now=True)


class Like(models.Model):
    author = models.ForeignKey(get_user_model(), null=True, on_delete=models.SET_NULL)
    post = models.ForeignKey(Post, related_name='likes', on_delete=models.CASCADE)