from django.urls import path

from core_api.veiws.photo_list_view.view import PhotoListView

urlpatterns = [
    path('photos/', PhotoListView.as_view()),
]
