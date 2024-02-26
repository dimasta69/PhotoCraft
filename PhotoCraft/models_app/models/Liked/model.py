from django.db import models

from models_app.models.photo.model import Photo
from models_app.models.users.model import User


class Liked(models.Model):
    photo_id = models.ForeignKey(Photo, on_delete=models.CASCADE, related_name='like', verbose_name='Фотография',
                              null=False)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='like', verbose_name='Пользователь',
                              null=False)

    class Meta:
        verbose_name = 'Лайк'
        verbose_name_plural = 'Лайки'
