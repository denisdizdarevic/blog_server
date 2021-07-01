from django.contrib.auth import get_user_model
from rest_framework import viewsets
from rest_framework.permissions import BasePermission, DjangoModelPermissionsOrAnonReadOnly

from blog.models import Post, Comment, Like, Tag, Attachment
from blog.serializers import PostSerializer, UserSerializer, CommentSerializer, LikeSerializer, TagSerializer, \
    AttachmentSerializer


class IsOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.author == request.user


class UserViewSet(viewsets.ModelViewSet):
    queryset = get_user_model().objects.all().order_by('id')
    serializer_class = UserSerializer


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all().order_by('timestamp_created')
    serializer_class = PostSerializer
    permission_classes = [IsOwner | DjangoModelPermissionsOrAnonReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all().order_by('id')
    serializer_class = TagSerializer


class AttachmentViewSet(viewsets.ModelViewSet):
    queryset = Attachment.objects.all().order_by('id')
    serializer_class = AttachmentSerializer


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all().order_by('timestamp')
    serializer_class = CommentSerializer
    permission_classes = [IsOwner | DjangoModelPermissionsOrAnonReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class LikeViewSet(viewsets.ModelViewSet):
    queryset = Like.objects.all().order_by('id')
    serializer_class = LikeSerializer
    permission_classes = [IsOwner | DjangoModelPermissionsOrAnonReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)