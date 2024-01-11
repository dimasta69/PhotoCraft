from django.db import models

from models_app.models.Photo.model import Photo
from models_app.models.Users.model import Users


class Liked(models.Model):
    id = models.AutoField(primary_key=True)
    photo_id = models.ForeignKey(Photo, on_delete=models.CASCADE, related_name='like', verbose_name='Фотография')
    users_id = models.ForeignKey(Users, on_delete=models.CASCADE, related_name='like', verbose_name='Пользователь')

    class Meta:
        verbose_name = 'Лайк'
        verbose_name_plural = 'Лайки'
