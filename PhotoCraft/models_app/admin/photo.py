from django.contrib import admin

from models_app.models.photo.model import Photo
from models_app.admin.comment import CommentAdmin


@admin.register(Photo)
class PhotoAdmin(admin.ModelAdmin):
    list_display = ['title', 'status', 'description', 'photo', 'backup_photo', 'category', 'user_id',
                    'publicated_at', 'updated_at', 'first_request_at', 'deleted_at']
    list_display_links = ['title']
    readonly_fields = ['backup_photo', 'user_id', 'publicated_at', 'updated_at', 'first_request_at', 'deleted_at',
                       'status']
    search_fields = ['title']
    list_filter = ['status']
    inlines = [CommentAdmin]
    save_on_top = True
    verbose_name = 'Фотография'
    verbose_name_plural = 'Фотографии'

    def accept_selected(self, request, queryset):
        for photo in queryset:
            photo.set_approve()

    def reject_selected(self, request, queryset):
        for photo in queryset:
            photo.set_reject()

    def deletion_selected(self, request, queryset):
        for photo in queryset:
            photo.set_schedule_deletion()

    def not_deletion_selected(self, request, queryset):
        for photo in queryset:
            photo.set_cancel_deletion()

    def has_delete_permission(self, request, obj=None):
        if not request.user.is_superuser and obj.status == 'Published':
            return False
        return True

    accept_selected.short_description = 'Принять выбранные'
    reject_selected.short_description = 'Отклонить выбранные'
    deletion_selected.short_description = 'Отправить на удаление'
    not_deletion_selected.short_description = 'Убрать задачу на удаление'

    actions = [accept_selected, reject_selected, deletion_selected, not_deletion_selected]
