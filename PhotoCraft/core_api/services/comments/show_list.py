from utils.services import ServiceWithResult

from django import forms
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator, EmptyPage

from functools import lru_cache

from models_app.models.photo.model import Photo
from models_app.models.comments.model import Comments

from photo_craft.settings.restframework import *


class CommentsListService(ServiceWithResult):
    photo_id = forms.IntegerField(required=True)
    per_page = forms.IntegerField(required=False)
    page = forms.IntegerField(required=False)

    custom_validations = ['photo_presence']

    def process(self):
        self.run_custom_validations()
        if self.is_valid():
            self.result = self._get_comments()
        return self

    def _get_comments(self):
        per_page = self.cleaned_data['per_page']
        page = self.cleaned_data['page']

        try:
            return Paginator(self.get_comment, per_page=(per_page or REST_FRAMEWORK['PAGE_SIZE'])).page(page or 1)
        except EmptyPage:
            return Paginator(self.get_comment.none(), per_page=(per_page or REST_FRAMEWORK['PAGE_SIZE'])).page(1)

    @property
    @lru_cache()
    def photo(self):
        try:
            return Photo.objects.get(id=self.cleaned_data['photo_id'])
        except Photo.DoesNotExist:
            return None

    @property
    @lru_cache()
    def comment(self):
        try:
            return Comments.objects.filter(photo_id=self.photo)
        except Comments.DoesNotExist:
            return Comments.objects.none()

    def photo_presence(self):
        if self.cleaned_data['photo_id']:
            if not self.photo:
                self.add_error('photo_id', ObjectDoesNotExist(f"Photo with id="
                                                              f"{self.cleaned_data['id']} not found"))
