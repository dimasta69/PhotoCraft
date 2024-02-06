from functools import lru_cache

from django import forms
from django.core.exceptions import ObjectDoesNotExist

from service_objects.fields import ModelField

from utils.services import ServiceWithResult
from models_app.models.users.model import User
from models_app.models.comments.model import Comments


class CommentUpdatedService(ServiceWithResult):
    id = forms.IntegerField(required=True)
    current_user = ModelField(User)
    text = forms.CharField(required=True)

    custom_validations = ['comment_presence', 'user_ratio']

    def process(self):
        self.run_custom_validations()
        if self.is_valid():
            self.result = self._update()
        return self

    def _update(self):
        comment = self.comment
        comment.text = self.cleaned_data['text']
        comment.updated_at = True
        comment.save()
        return comment

    @property
    @lru_cache()
    def comment(self):
        try:
            return Comments.objects.get(id=self.cleaned_data['id'])
        except Comments.DoesNotExist:
            return Comments.objects.none()

    def comment_presence(self):
        if self.cleaned_data['id']:
            if not self.comment:
                print(2)
                self.add_error('id', ObjectDoesNotExist(f"Comment with id="
                                                        f"{self.cleaned_data['id']} not found"))

    def user_ratio(self):
        if not ((self.comment.user_id.id == self.cleaned_data['current_user'].id) or
                self.cleaned_data['current_user'].is_superuser):
            self.add_error('current_user', ObjectDoesNotExist(f"User with id="
                                                              f"{self.cleaned_data['current_user']} is not the author "
                                                              f"of the post"))
