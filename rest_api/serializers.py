from rest_framework import serializers

from accounts.models import User
from blog.models import Post


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = (
            'date_created',
            'date_modified',
            'name',
            'email',
            'is_admin',
            'is_staff',
            'url',
        )


class PostAdminSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Post
        fields = (
            'title',
            'author',
            'date_created',
            'date_modified',
            'published',
            'title',
            'content',
            'summary',
            'slug'
        )

    def update(self, instance, validated_data):
        instance.published = validated_data.get('published', instance.published)
        instance.save()
