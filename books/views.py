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
    """
    Manages library books.
    list:
        Returns paginated list of all books.
        Supports search by title, category, author name.
        Supports ordering by created_at and available.
        Supports filtering via BookFilter (category, available, etc).
 
    create:
        Add a new book. Restricted to Librarians/Admins only.
 
    retrieve:
        Returns details of a specific book including image list
        and total active borrow count.
 
    update / partial_update:
        Update book details. Restricted to Librarians/Admins only.
 
    destroy:
        Delete a book. Restricted to Librarians/Admins only.
    """
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
    """
    Manages images for a specific book.
    Nested under books: /api/books/<book_pk>/images/
 
    list:
        Returns all images for the given book.
 
    create:
        Upload a new image for the given book.
        Restricted to Librarians/Admins only.
 
    destroy:
        Delete a book image. Restricted to Librarians/Admins only.
    """
    serializer_class = sz.BookImageSerializer
    permission_classes = [permissions.IsAdminOrReadOnly]

    def get_queryset(self):
        return BookImage.objects.filter(book_id=self.kwargs.get('book_pk'))
    
    def perform_create(self, serializer):
        serializer.save(book_id=self.kwargs.get('book_pk'))
        
class AuthorViewSet(ModelViewSet):
    """
    Manages authors.
    list:     Returns all authors.
    create:   Add a new author. Restricted to Librarians/Admins only.
    retrieve: Returns a specific author's details.
    update:   Update author info. Restricted to Librarians/Admins only.
    destroy:  Delete an author. Restricted to Librarians/Admins only.
    """
    queryset = Author.objects.prefetch_related('books').all()
    serializer_class = AuthorSerializer
    

class SpecificBookAuthorViewSet(ModelViewSet):
    """
    Returns the author of a specific book.
    Nested under books: /api/books/<book_pk>/author/
    list:
        Returns the author of the given book only.
        Read-only — no create, update, or delete allowed.
    """
    serializer_class = AuthorSerializer
    http_method_names = ['get']
    
    def get_queryset(self):
        return Author.objects.filter(books__id=self.kwargs.get('book_pk'))    