import asyncio

from django.db import models

from datetime import datetime

from django.db.models.signals import post_save
from django.dispatch import receiver
from django_fsm import FSMField, transition
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill

from models_app.models.categories.model import Categories
from models_app.models.users.model import User

from utils.file_uploader import uploaded_file_path

from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync


class Photo(models.Model):
    category_id = models.ForeignKey(Categories, on_delete=models.SET_NULL, related_name='photo', null=True, blank=True,
                                    verbose_name='Категория')
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='photo', verbose_name='Автор', null=False)

    title = models.CharField(max_length=100, null=False, verbose_name='Назавние')
    description = models.CharField(max_length=250, verbose_name='Описание', null=True)
    photo = models.ImageField(verbose_name='Фото', null=True, upload_to=uploaded_file_path)
    photo_space = ImageSpecField(source='photo',
                                 processors=[ResizeToFill(300, 165)],
                                 format='JPEG',
                                 options={'quality': 60})
    backup_photo = models.ImageField(verbose_name='Фотография до изменения', null=True, upload_to=uploaded_file_path)
    STATUS_CHOICES = (
        ('Moderation', 'Модерация'),
        ('Published', 'Опубликовано'),
        ('Reject', 'Отклонено'),
        ('Delete', 'Удаление'),
    )
    status = FSMField(choices=STATUS_CHOICES, default='Moderation')

    publicated_at = models.DateTimeField(verbose_name='Дата публикации', null=True)
    deleted_at = models.DateTimeField(verbose_name='Дата удаления', null=True)
    updated_at = models.DateTimeField(verbose_name='Дата обновления', null=True)
    first_request_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата запроса на публикацию')

    @transition(field=status, source=['Moderation', 'Reject'], target='Published')
    def set_approve(self):
        self.status = 'Published'
        if not self.publicated_at:
            self.publicated_at = datetime.now()
        else:
            self.updated_at = datetime.now()
        self.save()

    @transition(field=status, source='Moderation', target='Reject')
    def set_reject(self):
        self.status = 'Reject'
        self.save()

    @transition(field=status, source=['Published', 'Moderation', 'Reject'], target='Moderation')
    def set_update(self):
        self.status = 'Moderation'
        self.save()

    @transition(field=status, source='Published', target='Delete')
    def set_schedule_deletion(self):
        self.deleted_at = datetime.now()
        self.status = 'Delete'
        self.save()

    @transition(field=status, source='Delete', target='Published')
    def set_cancel_deletion(self):
        self.status = 'Published'
        self.deleted_at = None
        self.save()

    class Meta:
        verbose_name = 'Фотография'
        verbose_name_plural = 'Фотографии'

    def str(self):
        return self.title


@receiver(post_save, sender=Photo)
def send_notification(sender, instance, **kwargs):
    channel_layer = get_channel_layer()
    id = instance.id
    user_id = instance.user_id.id
    status = instance.status

    async def send_notification_async():
        await channel_layer.group_send(
            'name',
            {
                'type': 'change_status',
                'user_id': user_id,
                'status': status,
                'id': id
            }
        )

    asyncio.run(send_notification_async())
