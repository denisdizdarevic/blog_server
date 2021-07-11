from django.apps import AppConfig
from django.db.models.signals import post_migrate


class BlogConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'blog'

    def ready(self):
        post_migrate.connect(self.populate_models, sender=self)

    def populate_models(self, **kwargs):
        from django.contrib.auth import get_user_model
        from django.contrib.auth.models import Permission, Group
        from django.contrib.contenttypes.models import ContentType

        from blog.models import Post, Comment

        user_content_type = ContentType.objects.get_for_model(get_user_model())
        listing_permission, created = Permission.objects.get_or_create(codename='is_publicly_listed',
                                               name='Is publicly listed', content_type=user_content_type)

        post_content_type = ContentType.objects.get_for_model(Post)
        post_permissions = Permission.objects.filter(content_type=post_content_type).all()

        comment_content_type = ContentType.objects.get_for_model(Comment)
        comment_permissions = Permission.objects.filter(content_type=comment_content_type).all()

        author_group, created = Group.objects.get_or_create(name='Author')
        author_group_permissions = list(post_permissions) + list(comment_permissions) + [listing_permission]
        for perm in author_group_permissions:
            author_group.permissions.add(perm)

        user_group, created = Group.objects.get_or_create(name='User')
        for perm in comment_permissions:
            user_group.permissions.add(perm)
