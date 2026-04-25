from rest_framework import serializers
from decimal import Decimal
from books.models import Author, Book, BookImage

class BookImageSerializer(serializers.ModelSerializer):
    
    image = serializers.ImageField()
    class Meta:
        model = BookImage
        fields = ['id', 'image']
       
class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ['id', 'name', 'biography', 'created_at']
               
class BookSerializer(serializers.ModelSerializer):
    image = BookImageSerializer(many=True, read_only=True)
    author = AuthorSerializer(read_only=True)
    total_borrow_book = serializers.IntegerField(read_only=True)

    class Meta:
        model = Book
        fields = [
            'id', 'title', 'isbn', 'category', 
            'available', 'image', 'author', 
            'created_at', 'total_borrow_book'
        ]


