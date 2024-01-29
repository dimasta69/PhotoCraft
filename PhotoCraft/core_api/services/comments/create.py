from functools import lru_cache

from django import forms
from django.core.exceptions import ObjectDoesNotExist

from service_objects.fields import ModelField

from utils.services import ServiceWithResult
from models_app.models.users.model import User
from models_app.models.photo.model import Photo
from models_app.models.comments.model import Comments


class CommentCreateService(ServiceWithResult):
    photo_id = forms.IntegerField(required=True)
    current_user = ModelField(User)
    text = forms.CharField(required=True)
    reply_id = forms.IntegerField(required=False)

    custom_validations = ['photo_presence', 'reply_presence']

    def process(self):
        self.run_custom_validations()
        if self.is_valid():
            self.result = self._comment()
        return self

    def _comment(self):
        comment = Comments.objects.create(photo_id=self.get_photo,
                                          reply_id=self.get_reply,
                                          text=self.cleaned_data['text'],
                                          user_id=self.cleaned_data['current_user'])
        comment.save()
        return comment

    @property
    @lru_cache()
    def get_photo(self):
        try:
            return Photo.objects.get(id=self.cleaned_data['photo_id'])
        except Photo.DoesNotExist:
            return None

    @property
    @lru_cache()
    def get_reply(self):
        try:
            return Comments.objects.get(id=self.cleaned_data['reply_id'])
        except Comments.DoesNotExist:
            return None

    def photo_presence(self):
        if self.cleaned_data['photo_id']:
            if not self.get_photo:
                self.add_error('photo_id', ObjectDoesNotExist(f"Photo with id="
                                                              f"{self.cleaned_data['photo_id']} not found"))

    def reply_presence(self):
        if self.cleaned_data['reply_id']:
            if not self.get_reply:
                self.add_error('reply_id', ObjectDoesNotExist(f"Reply with id="
                                                              f"{self.cleaned_data['reply_id']} not found"))