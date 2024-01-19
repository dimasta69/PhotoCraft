from django.urls import path

from core_api.veiws.photo.photo_list.view import PhotoListView
from core_api.veiws.photo.photo.view import PhotoView
from core_api.veiws.categories.view import CategoriesView

urlpatterns = [
    path('photos/', PhotoListView.as_view()),
    path('categories/', CategoriesView.as_view()),
    path('photo/<int:id>', PhotoView.as_view()),
]
