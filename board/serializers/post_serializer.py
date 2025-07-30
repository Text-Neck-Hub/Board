

from rest_framework import serializers
from ..models import Post


class PostSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post

        fields = ['id', 'title', 'content', 'author',
                  'email', 'thumbnail', 'created_at', 'updated_at']

        read_only_fields = ['created_at', 'updated_at']

    def create(self, validated_data):
        post_instance = validated_data.pop('post')
        post = Post.objects.create(post=post_instance, **validated_data)
        return post
