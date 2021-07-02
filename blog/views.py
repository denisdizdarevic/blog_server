from django.contrib.auth import get_user_model
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import BasePermission, DjangoModelPermissionsOrAnonReadOnly
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_extensions.mixins import NestedViewSetMixin

from blog.filters import PostFilter
from blog.models import Post, Comment, Tag, Attachment
from blog.serializers import PostSerializer, UserSerializer, CommentSerializer, TagSerializer, AttachmentSerializer, \
    LikeSerializer


class IsOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.author == request.user


class UserViewSet(viewsets.ModelViewSet):
    queryset = get_user_model().objects.all().order_by('id')
    serializer_class = UserSerializer


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all().order_by('-timestamp_created')
    serializer_class = PostSerializer
    permission_classes = [IsOwner | DjangoModelPermissionsOrAnonReadOnly]
    filterset_class = PostFilter

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(detail=True, methods=['get'])
    def content(self, request, pk=None):
        return Response(self.get_object().content)

    @action(detail=True, methods=['post'], serializer_class=LikeSerializer)
    def like(self, request, pk=None):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.get_object().set_like(request.user, serializer.data.get('like', False))
        return Response('ok')


class TagViewSet(NestedViewSetMixin, viewsets.ModelViewSet):
    queryset = Tag.objects.all().order_by('id')
    serializer_class = TagSerializer

    def perform_create(self, serializer):
        serializer.save(post_id=self.kwargs['parent_lookup_post'])


class AttachmentViewSet(NestedViewSetMixin, viewsets.ModelViewSet):
    queryset = Attachment.objects.all().order_by('id')
    serializer_class = AttachmentSerializer

    def perform_create(self, serializer):
        serializer.save(post_id=self.kwargs['parent_lookup_post'])


class CommentViewSet(NestedViewSetMixin, viewsets.ModelViewSet):
    queryset = Comment.objects.all().order_by('timestamp')
    serializer_class = CommentSerializer
    permission_classes = [IsOwner | DjangoModelPermissionsOrAnonReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, post_id=self.kwargs['parent_lookup_post'])