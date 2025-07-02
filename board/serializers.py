from rest_framework import serializers
from .models import Board, Comment, Like


class BoardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Board
        fields = ['id', 'title', 'content', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at',
                            'updated_at']


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'content', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at',
                            'updated_at']


class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like.through
        fields = ['id', 'board', 'user', 'created_at']
        read_only_fields = fields
