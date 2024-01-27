from django.conf.urls.static import static
from django.urls import path

from core_api.veiws.photo.photo_list import PhotoListView
from core_api.veiws.photo.photo import PhotoView
from core_api.veiws.categories.category_list import CategoriesView
from core_api.veiws.liked.add_and_del import LikedView
from photo_craft import settings

urlpatterns = [
    path('photos/', PhotoListView.as_view()),
    path('categories/', CategoriesView.as_view()),
    path('photo/<int:id>', PhotoView.as_view()),
    path('like/', LikedView.as_view()),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
