from django.db import models
from django.db import transaction
from django.core.exceptions import ValidationError


class Board(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Board'
        verbose_name_plural = 'Boards'
        ordering = ['-created_at', '-updated_at']

    def create(self, *args, **kwargs):

        title = kwargs.get('title', '')
        if not title or title.strip() == '':
            raise ValidationError("Title cannot be empty")
        try:
            content = kwargs.get('content', '')
            Board.objects.create(title=title, content=content)
            super().save(*args, **kwargs)
        except Exception as e:
            raise ValidationError(f"Error saving Board: {str(e)}")


class Comment(models.Model):
    board = models.ForeignKey(
        Board, related_name='comments', on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Comment on {self.board.title}'

    class Meta:
        verbose_name = 'Comment'
        verbose_name_plural = 'Comments'
        ordering = ['-created_at', ' -updated_at']


class Like(models.Model):
    board = models.ForeignKey(
        Board, related_name='likes', on_delete=models.CASCADE)

    user = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Like by {self.user} on {self.board.title}'

    class Meta:
        verbose_name = 'Like'
        verbose_name_plural = 'Likes'
        unique_together = ('board', 'user')
        ordering = ['-created_at']


# class Category(models.Model):
#     name = models.CharField(max_length=50, unique=True)
#     description = models.TextField(blank=True, null=True)

#     def __str__(self):
#         return self.name

#     class Meta:
#         verbose_name = 'Category'
#         verbose_name_plural = 'Categories'
#         ordering = ['name']
