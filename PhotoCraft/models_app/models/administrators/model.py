from models_app.models.users.model import Users


class Administrators(Users):
    class Meta:
        proxy = True
        verbose_name = 'Администратор'
        verbose_name_plural = 'Администраторы'
