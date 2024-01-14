from django.urls import path

from core_api.veiws.photo_list_view.view import PhotoListView
from core_api.veiws.categories_view.view import CategoriesView

urlpatterns = [
    path('photos/', PhotoListView.as_view()),
    path('categories/', CategoriesView.as_view()),
]
