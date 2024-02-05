from django.conf.urls.static import static
from django.urls import path, include, re_path

from core_api.veiws.photo.photo_list import PhotoListView
from core_api.veiws.photo.photo import PhotoView
from core_api.veiws.categories.category_list import CategoriesView
from core_api.veiws.categories.show import CategoryView
from core_api.veiws.liked.add_and_del import LikedView
from core_api.veiws.comments.show_list import CommentsView
from core_api.veiws.comments.show import CommentView
from core_api.veiws.photo.personal_area import PersonalAreaView
from photo_craft import settings

urlpatterns = [
    path('photos/', PhotoListView.as_view()),
    path('categories/', CategoriesView.as_view()),
    path('category/<int:id>/', CategoryView.as_view()),
    path('photo/<int:id>/', PhotoView.as_view()),
    path('like/', LikedView.as_view()),
    path('comments/', CommentsView.as_view()),
    path('comment/<int:id>/', CommentView.as_view()),
    path('profile/', PersonalAreaView.as_view()),
    path('auth/', include('djoser.urls')),
    re_path(r'^auth/', include('djoser.urls.authtoken')),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
