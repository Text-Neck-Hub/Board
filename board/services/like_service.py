from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction

from ..models import Like, Post


class LikeService:
    @staticmethod
    def add_like(user_id: int, post_id: int) -> Like:
        try:
            post = Post.objects.get(id=post_id)
        except ObjectDoesNotExist:
            raise ValueError("해당 게시글이 존재하지 않습니다.")

        if Like.objects.filter(user=user_id, post=post).exists():
            raise ValueError("이미 좋아요를 누른 게시글입니다.")

        with transaction.atomic():
            like = Like.objects.create(user=user_id, post=post)
        return like

    @staticmethod
    def remove_like(user_id: int, post_id: int):
        try:
            post = Post.objects.get(id=post_id)
        except ObjectDoesNotExist:
            raise ValueError("해당 게시글이 존재하지 않습니다.")

        try:
            like = Like.objects.get(user=user_id, post=post)
        except ObjectDoesNotExist:
            raise ValueError("해당 게시글에 좋아요를 누르지 않았습니다.")

        with transaction.atomic():
            like.delete()
