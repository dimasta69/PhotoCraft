from django.db import models

from models_app.models.photo.model import Photo
from models_app.models.users.model import User


class Comments(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comment', verbose_name='Пользователь',
                             null=False)
    reply = models.ForeignKey('self', on_delete=models.CASCADE, related_name='replies',
                              verbose_name='Ответ на коментарий', null=True, blank=True)
    photo = models.ForeignKey(Photo, on_delete=models.CASCADE, related_name='comment', verbose_name='Фотография',
                              null=False)

    text = models.CharField(max_length=200, null=False)

    publicated_at = models.DateTimeField(auto_now_add=True, null=False, verbose_name='Дата публикации')
    updated_at = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
