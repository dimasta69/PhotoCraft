from models_app.models.users.model import User


class Authors(User):
    class Meta:
        proxy = True
        verbose_name = 'Автор'
        verbose_name_plural = 'Авторы'
