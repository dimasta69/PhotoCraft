from models_app.models.users.model import Users


class Authors(Users):
    class Meta:
        proxy = True
        verbose_name = 'Автор'
        verbose_name_plural = 'Авторы'
