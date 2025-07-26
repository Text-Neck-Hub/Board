

# class CommentSerializer(serializers.ModelSerializer):
#     author = serializers.IntegerField(read_only=True)

#     class Meta:
#         model = Comment
#         fields = ['id', 'post', 'author',
#                   'content', 'created_at', 'updated_at']
#         read_only_fields = ['id', 'post', 'created_at', 'updated_at']

#     def get_author(self, obj):
#         return obj.author


# class LikeSerializer(serializers.ModelSerializer):
#     user = serializers.IntegerField(read_only=True)

#     class Meta:
#         model = Like
#         fields = '__all__'
