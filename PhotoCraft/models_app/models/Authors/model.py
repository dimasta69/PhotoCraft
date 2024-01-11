from models_app.models.Users.model import Users


class Authors(Users):
    class Meta:
        proxy = True
        verbose_name = 'Автор'
        verbose_name_plural = 'Авторы'
