from django.contrib import admin
from models_app.models.photo.model import Photo


class PhotoAdmin(admin.ModelAdmin):
    list_display = ('id', 'category_id', 'user_id', 'title', 'description', 'photo', 'backup_photo', 'status',
                    'publicated_at', 'deleted_at', 'updated_at', 'first_request_at')

    # def get_queryset(self, request):
    #     return super().get_queryset(request).filter(status='Moderation')


admin.site.register(Photo, PhotoAdmin)
