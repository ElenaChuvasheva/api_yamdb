from django.urls import include, path
from rest_framework import routers

from api.views import (CategoryViewSet, CommentViewSet, CustomUserViewSet,
                       GenreViewSet, ReviewViewSet, TitleViewSet,
                       get_auth_token, signup)

app_name = 'api'

v1_router = routers.DefaultRouter()
v1_router.register(r'titles/(?P<title_id>\d+)/reviews',
                   ReviewViewSet, basename='review')
v1_router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet, basename='comment')
v1_router.register('users', CustomUserViewSet)
v1_router.register('categories', CategoryViewSet, basename='categories')
v1_router.register('genres', GenreViewSet, basename='genres')
v1_router.register('titles', TitleViewSet, basename='titles')

urlpatterns = [
    path('v1/', include(v1_router.urls)),
    path('v1/auth/signup/', signup, name='signup'),
    path('v1/auth/token/', get_auth_token, name='authtoken'),
]
