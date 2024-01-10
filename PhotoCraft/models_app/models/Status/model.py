from django.db import models


class Status(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=150, null=False, verbose_name='Название')

    class Meta:
        verbose_name = 'Статус'
        verbose_name_plural = "Статусы"

    def __str__(self):
        return self.title
