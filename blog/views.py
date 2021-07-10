from django.contrib.auth import get_user_model
from django.db.models import Q
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import BasePermission, DjangoModelPermissionsOrAnonReadOnly, SAFE_METHODS, IsAdminUser, \
    DjangoModelPermissions, IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.schemas.openapi import AutoSchema
from rest_framework_extensions.mixins import NestedViewSetMixin

from blog.filters import PostFilter
from blog.models import Post, Comment, Tag, Attachment
from blog.serializers import PostSerializer, UserSerializer, CommentSerializer, TagSerializer, AttachmentSerializer, \
    LikeSerializer


class IsOwnerOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True

        return obj.author == request.user


class IsPostOwnerOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if view.action == "create":
            if 'parent_lookup_post' not in view.kwargs:
                return False
            parent_post = Post.objects.get(id=view.kwargs['parent_lookup_post'])
            return parent_post.author == request.user
        else:
            return True

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True

        return obj.post.author == request.user


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = get_user_model().objects.filter(Q(user_permissions__codename="is_publicly_listed") |
                                               Q(groups__permissions__codename="is_publicly_listed"))\
                                            .distinct().order_by('id')
    serializer_class = UserSerializer


class TagListView(viewsets.ViewSet):
    permission_classes = [AllowAny]

    def list(self, request):
        return Response(Tag.objects.values_list('name', flat=True).distinct().all())


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all().order_by('-timestamp_created')
    serializer_class = PostSerializer
    permission_classes = [(IsOwnerOrReadOnly & DjangoModelPermissionsOrAnonReadOnly) | IsAdminUser]
    filterset_class = PostFilter

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(detail=True, methods=['get'])
    def content(self, request, pk=None):
        return Response(self.get_object().content)

    @action(detail=True, methods=['post'], serializer_class=LikeSerializer, permission_classes=[IsAuthenticated])
    def like(self, request, pk=None):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.get_object().set_like(request.user, serializer.data.get('like', False))
        return Response('ok')


class TagViewSet(NestedViewSetMixin, viewsets.ModelViewSet):
    queryset = Tag.objects.all().order_by('id')
    serializer_class = TagSerializer
    permission_classes = [(IsPostOwnerOrReadOnly & DjangoModelPermissionsOrAnonReadOnly) | IsAdminUser]
    schema = AutoSchema(operation_id_base='PostTag')

    def perform_create(self, serializer):
        serializer.save(post_id=self.kwargs['parent_lookup_post'])


class AttachmentViewSet(NestedViewSetMixin, viewsets.ModelViewSet):
    queryset = Attachment.objects.all().order_by('id')
    serializer_class = AttachmentSerializer
    permission_classes = [(IsPostOwnerOrReadOnly & DjangoModelPermissionsOrAnonReadOnly) | IsAdminUser]
    schema = AutoSchema(operation_id_base='PostAttachment')

    def perform_create(self, serializer):
        serializer.save(post_id=self.kwargs['parent_lookup_post'])


class CommentViewSet(NestedViewSetMixin, viewsets.ModelViewSet):
    queryset = Comment.objects.all().order_by('timestamp')
    serializer_class = CommentSerializer
    permission_classes = [(IsOwnerOrReadOnly & DjangoModelPermissionsOrAnonReadOnly) | IsAdminUser]
    schema = AutoSchema(operation_id_base='PostComment')

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, post_id=self.kwargs['parent_lookup_post'])
