from django.db import models


class Categories(models.Model):
    title = models.CharField(max_length=150, null=False, verbose_name="Название")

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = "Категории"

    def __str__(self):
        return self.title
