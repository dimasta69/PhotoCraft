from utils.services import ServiceWithResult

from django import forms
from django.core.exceptions import ObjectDoesNotExist

from functools import lru_cache

from models_app.models.comments.model import Comments


class CommentService(ServiceWithResult):
    id = forms.IntegerField(required=True)

    custom_validations = ['comment_presence']

    def process(self):
        self.run_custom_validations()
        if self.is_valid():
            self.result = self.get_comment
        return self

    @property
    @lru_cache()
    def get_comment(self):
        try:
            return Comments.objects.get(id=self.cleaned_data['id'])
        except Comments.DoesNotExist:
            return Comments.objects.none()

    def comment_presence(self):
        if self.cleaned_data['id']:
            if not self.get_comment:
                self.add_error('id', ObjectDoesNotExist(f"Comment with id="
                                                        f"{self.cleaned_data['id']} not found"))
