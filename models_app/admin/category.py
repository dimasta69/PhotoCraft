from django.contrib import admin

from models_app.models.categories.model import Categories


@admin.register(Categories)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['title']
    search_fields = ['title']