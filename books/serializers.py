from rest_framework import serializers
from decimal import Decimal
from books.models import Author, Book, BorrowRecord, Member

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['id', 'title', 'isbn', 'category', 'available', 'author', 'created_at', 'total_borrow_book']
        
    total_borrow_book = serializers.SerializerMethodField(
        method_name='calculate_borrow_book')
    
    def calculate_borrow_book(self, book):
           return book.borrow_records.filter(status='borrowed').count()
       
class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ['id', 'name', 'biography', 'created_at']
        

