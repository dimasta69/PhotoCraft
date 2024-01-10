from django.db import models

from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill

from models_app.models.Categories.model import Categories
from models_app.models.Status.model import Status
from models_app.models.Users.model import Users


class Photo(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100, null=False, verbose_name='Назавние')
    description = models.CharField(max_length=250, verbose_name='Описание')
    user_id = models.ForeignKey(Users, on_delete=models.CASCADE, related_name='photo', verbose_name='Автор')
    publicated_at = models.DateField(verbose_name='Дата публикации')
    deleted_at = models.DateField(verbose_name='Дата удаления')
    updated_at = models.DateField(verbose_name='Дата обновления')
    request_at = models.DateField(auto_now_add=True, verbose_name='Дата запроса на публикацию')
    photo = models.ImageField(verbose_name='Фото')
    photo_space = ImageSpecField(source='photo',
                                 processors=[ResizeToFill(300, 165)],
                                 format='JPEG',
                                 options={'quality': 60})
    backup_photo = models.ImageField(verbose_name='Фотография до изменения')
    category_id = models.ForeignKey(Categories, on_delete=models.SET_NULL, related_name='photo',
                                    verbose_name='Категория')
    status_id = models.ForeignKey(Status, on_delete=models.SET_NULL, related_name='photo',
                                  verbose_name='Статус')

    class Meta:
        verbose_name = 'Фотография'
        verbose_name_plural = 'Фотографии'

    def __str__(self):
        return self.title

