import factory
from django.core.files.uploadedfile import SimpleUploadedFile
from factory.django import DjangoModelFactory

from models_app.models.photo.model import Photo
from models_app.models.users.model import User
from models_app.models.categories.model import Categories

from utils.file_uploader import uploaded_file_path


class PhotoFactory(DjangoModelFactory):
    class Meta:
        model = Photo

    category_id = factory.Iterator(Categories.objects.all().values_list('id', flat=True))
    user_id = factory.Iterator(User.objects.all().values_list('id', flat=True))
    title = factory.Faker('sentence', nb_words=3)
    description = factory.Faker('text', max_nb_chars=250)
    status = factory.Iterator(['Moderation', 'Published', 'Reject', 'Delete'])

    @factory.post_generation
    def add_photo(self, create, extracted, **kwargs):
        if create:
            self.save()
            path = uploaded_file_path(self, "example.jpg")
            image = factory.django.ImageField()._make_data({"width": 300, "height": 165})
            file = SimpleUploadedFile(name='example.jpg', content=image, content_type='image/jpeg')
            self.photo.save(path, file)
