from django.db import models
from django.contrib.auth import get_user_model
from shortuuid import uuid


class Post(models.Model):
    title = models.TextField()
    slug = models.SlugField(unique=True, null=False)
    description = models.TextField()
    content = models.TextField()
    author = models.ForeignKey(get_user_model(), null=True, on_delete=models.SET_NULL)
    timestamp_created = models.DateTimeField(auto_now_add=True)
    timestamp_edited = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = uuid()
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.title} ({self.slug})'

    def get_like(self, user):
        return self.likes.filter(author__exact=user)

    def set_like(self, user, like):
        like_query = self.get_like(user)
        if like == False and like_query.exists():
            like_query.delete()
        elif like == True and not like_query.exists():
            Like.objects.create(author=user, post=self).save()


class Tag(models.Model):
    name = models.TextField()
    post = models.ForeignKey(Post, related_name='tags', on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Attachment(models.Model):
    file = models.FileField(upload_to='uploads/%Y/%m/%d/')
    post = models.ForeignKey(Post, related_name='attachments', on_delete=models.CASCADE)


class Comment(models.Model):
    content = models.TextField()
    author = models.ForeignKey(get_user_model(), null=True, on_delete=models.SET_NULL)
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now=True)


class Like(models.Model):
    author = models.ForeignKey(get_user_model(), null=True, on_delete=models.SET_NULL)
    post = models.ForeignKey(Post, related_name='likes', on_delete=models.CASCADE)
