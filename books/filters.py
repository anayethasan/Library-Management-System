from django_filters.rest_framework import FilterSet
from books.models import Book

class BookFilter(FilterSet):
    class Meta:
        model = Book
        fields = {
            'author_id': ['exact'],
            'available': ['exact'],
            'created_at': ['exact', 'date__gte', 'date__lte']
        }
    
    