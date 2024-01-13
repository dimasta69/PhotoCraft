from django.urls import path

from core_api.veiws.photo_list_view.view import PhotoListView
from core_api.veiws.category_view.view import CategoryView

urlpatterns = [
    path('photos/', PhotoListView.as_view()),
    path('categories/', CategoryView.as_view()),
]
