from django.db import models
from .utils.file_uploader import post_thumbnail_upload_to


class Board(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True,
                            help_text="URL에 사용될 고유한 이름 (예: free, qna)")
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField(default='', null=True, blank=True)
    author = models.IntegerField(null=False, blank=False)
    email = models.EmailField(
        default='test@example.com', null=False, blank=False, db_index=True)
    board = models.ForeignKey(
        Board, on_delete=models.CASCADE, related_name='posts')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    thumbnail = models.ImageField(
        upload_to=post_thumbnail_upload_to, blank=True, null=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Post by {self.author.username if hasattr(self.author, 'username') else self.author.email}: {self.title}"


class AttachedFile(models.Model):
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name='attachments')
    file = models.FileField(upload_to='post_attachments/')
    file_name = models.CharField(max_length=255, blank=True)
    file_size = models.PositiveIntegerField(default=0)
    mimetype = models.CharField(max_length=100, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.file_name if self.file_name else self.file.name

    def delete(self, *args, **kwargs):
        self.file.delete()
        super().delete(*args, **kwargs)


class Comment(models.Model):
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name='comments')
    author = models.IntegerField(
        null=False, blank=False)
    email = models.EmailField(
        default='test@example.com', null=False, blank=False, db_index=True)
    content = models.TextField(default='', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f"Comment by {self.author.username if hasattr(self.author, 'username') else self.author.email} on {self.post.title[:30]}..."


class Like(models.Model):
    user = models.IntegerField(
        null=False, blank=False)
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name='likes')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'post')
        indexes = [
            models.Index(fields=['user', 'post']),
            models.Index(fields=['post']),
        ]

    def __str__(self):
        return f"User {self.user.username if hasattr(self.user, 'username') else self.user.email} likes {self.post.title}"
