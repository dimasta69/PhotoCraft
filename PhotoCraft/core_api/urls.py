from django.conf.urls.static import static
from django.urls import path

from djoser.views import TokenCreateView, TokenDestroyView, UserViewSet

from core_api.veiws.photo.photo_list import PhotoListView
from core_api.veiws.photo.photo import PhotoView
from core_api.veiws.categories.category_list import CategoriesView
from core_api.veiws.categories.show import CategoryView
from core_api.veiws.liked.add_and_del import LikedView
from core_api.veiws.comments.show_list import CommentsView
from core_api.veiws.comments.show import CommentView
from core_api.veiws.profile.show import ProfileView
from photo_craft import settings

urlpatterns = [
    path('photos/', PhotoListView.as_view()),
    path('categories/', CategoriesView.as_view()),
    path('category/<int:id>/', CategoryView.as_view()),
    path('photo/<int:id>/', PhotoView.as_view()),
    path('like/', LikedView.as_view()),
    path('comments/', CommentsView.as_view()),
    path('comment/<int:id>/', CommentView.as_view()),
    path('profile/', ProfileView.as_view()),
    path('auth/users/', UserViewSet.as_view({'post': 'create'}), name='user-create'),
    path('auth/token/login/', TokenCreateView.as_view()),
    path('auth/token/logout/', TokenDestroyView.as_view()),
    path('auth/token/refresh/', TokenCreateView.as_view()),
    path('auth/users/activation/', UserViewSet.as_view({'post': 'activate'})),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

#  path('auth/', include('djoser.urls')),
#  re_path(r'^auth/', include('djoser.urls.authtoken')),
