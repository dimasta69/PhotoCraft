from django.db import models

from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill

from models_app.models.categories.model import Categories
from models_app.models.users.model import User

from utils.file_uploader import uploaded_file_path


class Photo(models.Model):
    category = models.ForeignKey(Categories, on_delete=models.SET_NULL, related_name='photo', null=True,
                                    verbose_name='Категория')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='photo', verbose_name='Автор', null=False)

    title = models.CharField(max_length=100, null=False, verbose_name='Назавние')
    description = models.CharField(max_length=250, verbose_name='Описание', null=True)
    photo = models.ImageField(verbose_name='Фото', null=True, upload_to=uploaded_file_path)
    photo_space = ImageSpecField(source='photo',
                                 processors=[ResizeToFill(300, 165)],
                                 format='JPEG',
                                 options={'quality': 60})
    backup_photo = models.ImageField(verbose_name='Фотография до изменения', null=True, upload_to=uploaded_file_path)
    STATUS_CHOICES = (
        ('на модерации', 'На модерации'),
        ('одобренно', 'Одобрено'),
        ('на удалении', 'На удалении'),
    )
    status = models.CharField(choices=STATUS_CHOICES, default='на модерации', editable=False)

    publicated_at = models.DateField(verbose_name='Дата публикации', null=True)
    deleted_at = models.DateField(verbose_name='Дата удаления', null=True)
    updated_at = models.DateField(verbose_name='Дата обновления', null=True)
    request_at = models.DateField(auto_now_add=True, verbose_name='Дата запроса на публикацию')

    class Meta:
        verbose_name = 'Фотография'
        verbose_name_plural = 'Фотографии'

    def __str__(self):
        return self.title
