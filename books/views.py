from books.models import Book, Author, BookImage
from django.db.models import Q, Count
from books.serializers import BookSerializer, AuthorSerializer
from rest_framework.viewsets import ModelViewSet
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from books.filters import BookFilter
from books.pagination import DefaultPagination
from books import serializers as sz
from api import permissions

class BookViewSet(ModelViewSet):
    queryset = Book.objects.select_related('author').prefetch_related('image').annotate(
            total_borrow_book=Count(
                'borrow_records',
                filter=Q(borrow_records__status='borrowed')
            )
        )
    serializer_class = BookSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = BookFilter
    pagination_class = DefaultPagination
    
    search_fields = ['title', 'category', 'author__name']
    ordering_fields = ['created_at', 'available']
    ordering = ['-available', 'title']
    
class BookImageViewSet(ModelViewSet):
    serializer_class = sz.BookImageSerializer
    permission_classes = [permissions.IsAdminOrReadOnly]

    def get_queryset(self):
        return BookImage.objects.filter(book_id=self.kwargs.get('book_pk'))
    
    def perform_create(self, serializer):
        serializer.save(book_id=self.kwargs.get('book_pk'))
        
class AuthorViewSet(ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    

class SpecificBookAuthorViewSet(ModelViewSet):
    serializer_class = AuthorSerializer
    http_method_names = ['get']
    
    def get_queryset(self):
        return Author.objects.filter(books__id=self.kwargs.get('book_pk'))    