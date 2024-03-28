from functools import lru_cache

from django import forms
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status

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
            self.result = self._update_comment()
            self.response_status = status.HTTP_201_CREATED
        return self

    def _update_comment(self) -> Comments:
        self.comment.text = self.cleaned_data['text']
        self.comment.updated_at = True
        self.comment.save()
        return self.comment

    @property
    @lru_cache()
    def comment(self) -> Comments:
        try:
            return Comments.objects.get(id=self.cleaned_data['id'])
        except Comments.DoesNotExist:
            return Comments.objects.none()

    def comment_presence(self):
        if self.cleaned_data['id']:
            if not self.comment:
                self.add_error('id', ObjectDoesNotExist(f"Comment with id="
                                                        f"{self.cleaned_data['id']} not found"))
                self.response_status = status.HTTP_404_NOT_FOUND

    def user_ratio(self):
        if not ((self.comment.user.id == self.cleaned_data['current_user'].id) or
                self.cleaned_data['current_user'].is_superuser):
            self.add_error('current_user', ObjectDoesNotExist(f"User with id="
                                                              f"{self.cleaned_data['current_user']} is not the author "
                                                              f"of the post"))
            self.response_status = status.HTTP_403_FORBIDDEN
