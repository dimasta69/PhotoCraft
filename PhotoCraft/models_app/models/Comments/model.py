from django.db import models

from models_app.models.Photo.model import Photo
from models_app.models.Users.model import Users


class Comments(models.Model):
    id = models.AutoField(primary_key=True)
    publicated_at = models.DateField(auto_now_add=True, null=False, verbose_name='Дата публикации')
    updated_at = models.DateField()
    text = models.CharField(max_length=200, null=False)
    user_id = models.ForeignKey(Users, on_delete=models.CASCADE, related_name='comment', verbose_name='Пользователь')
    reply_id = models.IntegerField(verbose_name='Ответ на комментарий')
    photo_id = models.ForeignKey(Photo, on_delete=models.CASCADE, related_name='comment', verbose_name='Фотография')

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
