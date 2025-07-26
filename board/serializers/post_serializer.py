from rest_framework import serializers
from ..models import Post, AttachedFile, Like


class AttachedFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = AttachedFile
        fields = ['id', 'file', 'file_name',
                  'file_size', 'mimetype', 'uploaded_at']
        read_only_fields = ['id', 'file', 'file_name',
                            'file_size', 'mimetype', 'uploaded_at']


class PostSerializer(serializers.ModelSerializer):
    author = serializers.IntegerField(read_only=True)
    board_slug = serializers.SlugField(write_only=True, required=False)
    likes_count = serializers.SerializerMethodField()
    is_liked = serializers.SerializerMethodField()
    attachments = AttachedFileSerializer(many=True, read_only=True)
    thumbnail = serializers.ImageField(read_only=True)

    class Meta:
        model = Post
        fields = ['id', 'title', 'content', 'author', 'board_slug', 'created_at',
                  'updated_at', 'likes_count', 'is_liked', 'thumbnail', 'attachments']
        read_only_fields = ['id', 'author',
                            'created_at', 'updated_at', 'thumbnail']

    def get_author(self, obj):
        return obj.author

    def get_likes_count(self, obj):
        return obj.likes.count()

    def get_is_liked(self, obj):
        request = self.context.get('request', None)
        if request and request.user.is_authenticated:
            user_id = getattr(request.user, 'id', None)
            if user_id is not None:
                return Like.objects.filter(post=obj, user=user_id).exists()
        return False
