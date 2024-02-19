from django.contrib import admin

from models_app.models.users.model import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'first_name', 'last_name', 'is_active', 'is_staff', 'is_superuser',
                    'date_joined']
    list_filter = ['is_superuser', 'is_staff', 'is_active']
    verbose_name = 'Пользователь'
    verbose_name_plural = 'Пользователи'