from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_nested import routers
from books.views import BookViewSet, AuthorViewSet, BookImageViewSet, SpecificBookAuthorViewSet
from member.views import MemberViewSet
from borrow.views import BorrowRecordViewSet
from borrow.dashboard import (
    TotalBooksView,
    TotalMembersView,
    BorrowedBooksView,
    AvailableBooksView
)


router = routers.DefaultRouter()
router.register('books', BookViewSet, basename='books')
router.register('authors', AuthorViewSet, basename='authors')
router.register('members', MemberViewSet, basename='members')
router.register('borrow', BorrowRecordViewSet, basename='borrow')

book_router = routers.NestedDefaultRouter(
    router, 'books', lookup='book'
)
book_router.register('images', BookImageViewSet, basename='book-images')
book_router.register('author', SpecificBookAuthorViewSet, basename='book-author')

urlpatterns = [
    path('', include(router.urls)),
    path('', include(book_router.urls)),
    
    path('dashboard/total-books/', TotalBooksView.as_view(), name='dashboard-total-books'),
    path('dashboard/total-members/', TotalMembersView.as_view(), name='dashboard-total-members'),
    path('dashboard/borrowed-books/', BorrowedBooksView.as_view(), name='dashboard-borrowed-books'),
    path('dashboard/available-books/', AvailableBooksView.as_view(), name='dashboard-available-books'),
    
    path('auth/', include('users.urls')),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
]

