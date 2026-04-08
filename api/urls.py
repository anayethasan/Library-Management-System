from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_nested import routers
from books.views import BookViewSet, AuthorViewSet

router = routers.DefaultRouter()
router.register('books', BookViewSet, basename='books')
router.register('authors', AuthorViewSet, basename='authors')


urlpatterns = [
    path('', include(router.urls)),
]

