from models_app.models.users.model import User


class Administrators(User):
    class Meta:
        proxy = True
        verbose_name = 'Администратор'
        verbose_name_plural = 'Администраторы'
