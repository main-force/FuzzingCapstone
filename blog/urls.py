from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PostViewSet, ReplyViewSet

router = DefaultRouter(trailing_slash=False)
router.register(r'posts', PostViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('posts/<int:post_id>/reply', ReplyViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('posts/<int:post_id>/reply/<int:pk>', ReplyViewSet.as_view({'get': 'retrieve', 'delete': 'destroy'})),
]
