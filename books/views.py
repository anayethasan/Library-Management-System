from rest_framework.response import Response
from books.models import Book, Author, BorrowRecord, Member
from books.serializers import BookSerializer, AuthorSerializer
from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from books.filters import BookFilter
from books.pagination import DefaultPagination


class BookViewSet(ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = BookFilter
    pagination_class = DefaultPagination
    
    search_fields = ['title', 'category', 'author__name']
    ordering_fields = ['created_at', 'available']
    ordering = ['-available', 'title']
    

class AuthorViewSet(ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    
    