from django.db import models

from datetime import datetime

from django_fsm import FSMField, transition
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill

from models_app.models.categories.model import Categories
from models_app.models.users.model import User

from utils.file_uploader import uploaded_file_path


class Photo(models.Model):
    category_id = models.ForeignKey(Categories, on_delete=models.SET_NULL, related_name='photo', null=True, blank=True,
                                    verbose_name='Категория')
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='photo', verbose_name='Автор', null=False)
    scheduled_deletion_task_id = models.CharField(max_length=255, null=True, blank=True)

    title = models.CharField(max_length=100, null=False, verbose_name='Назавние')
    description = models.CharField(max_length=250, verbose_name='Описание', null=True)
    photo = models.ImageField(verbose_name='Фото', null=True, upload_to=uploaded_file_path)
    photo_space = ImageSpecField(source='photo',
                                 processors=[ResizeToFill(300, 165)],
                                 format='JPEG',
                                 options={'quality': 60})
    backup_photo = models.ImageField(verbose_name='Фотография до изменения', null=True, upload_to=uploaded_file_path)
    STATUS_CHOICES = (
        ('Moderation', 'moderation'),
        ('Published', 'published'),
        ('Reject', 'reject'),
        ('Delete', 'delete'),
    )
    status = FSMField(choices=STATUS_CHOICES, default='Moderation')

    publicated_at = models.DateField(verbose_name='Дата публикации', null=True)
    deleted_at = models.DateField(verbose_name='Дата удаления', null=True)
    updated_at = models.DateField(verbose_name='Дата обновления', null=True)
    request_at = models.DateField(auto_now_add=True, verbose_name='Дата запроса на публикацию')

    @transition(field=status, source='Moderation', target='Published')
    def approve(self):
        self.status = 'Published'
        if not self.publicated_at:
            self.publicated_at = datetime.now()
        else:
            self.updated_at = datetime.now()

    @transition(field=status, source='Moderation', target='Rejected')
    def reject(self):
        self.status = 'Reject'
        self.save()

    @transition(field=status, source=['Published', 'Moderation', 'Rejected'], target='Moderation')
    def update(self):
        self.status = 'Moderation'
        self.save()

    # @transition(field=status, source='Published', target='Delete')
    @transition(field=status, source=['Published', 'Moderation'], target='Delete')
    def schedule_deletion(self):
        self.deleted_at = datetime.now()
        self.status = 'Delete'
        self.save()

    @transition(field=status, source='Delete', target='Published')
    def cancel_deletion(self):
        self.status = 'Published'
        self.deleted_at = None
        self.save()

    class Meta:
        verbose_name = 'Фотография'
        verbose_name_plural = 'Фотографии'

    def __str__(self):
        return self.title
