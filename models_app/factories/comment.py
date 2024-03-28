import factory
from factory.django import DjangoModelFactory

from models_app.models.comments.model import Comments
from models_app.models.users.model import User
from models_app.models.photo.model import Photo


class CommentFactory(DjangoModelFactory):
    class Meta:
        model = Comments

    photo = factory.Iterator(Photo.objects.all().values_list('id', flat=True))
    user = factory.Iterator(User.objects.all().values_list('id', flat=True))
    text = factory.Faker('text', max_nb_chars=200)

    @factory.post_generation
    def reply(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            if isinstance(extracted, Comments):
                self.reply = extracted
        else:
            pass