from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from rest_framework import serializers
from taggit.serializers import TagListSerializerField

from blog.models import Post, Comment


class UserSerializer(serializers.ModelSerializer):
    groups = serializers.StringRelatedField(many=True, read_only=True)

    class Meta:
        model = get_user_model()
        fields = ['id', 'username', 'email', 'groups', 'first_name', 'last_name']


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ['id', 'name']


class CommentSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ['post']


class PostSerializer(serializers.ModelSerializer):
    tags = TagListSerializerField()
    like_me = serializers.SerializerMethodField()
    like_count = serializers.SerializerMethodField()
    comment_count = serializers.SerializerMethodField()
    author = UserSerializer(read_only=True)

    class Meta:
        model = Post
        fields = '__all__'
        read_only_fields = ['author']
        extra_kwargs = {
            'content': {'write_only': True}
        }

    def get_like_me(self, obj: Post):
        if self.context['request'].user.is_authenticated:
            return obj.get_like(self.context['request'].user).exists()
        else:
            return False

    def get_comment_count(self, obj: Post):
        return obj.comments.count()

    def get_like_count(self, obj: Post):
        return obj.likes.count()


class LikeSerializer(serializers.Serializer):
    like = serializers.BooleanField()
