from django.contrib import admin

from models_app.models.comments.model import Comments


class CommentAdmin(admin.StackedInline):
    model = Comments
    extra = 1
    readonly_fields = ['user_id', 'reply_id', 'publicated_at', 'updated_at']
