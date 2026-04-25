from django.db import models
from cloudinary.models import CloudinaryField
from books.validators import validate_file_size
from member.models import Member

        
class Author(models.Model):
    name = models.CharField(max_length=250)
    biography = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['name']
        

class Book(models.Model):
    CATEGORY_CHOICES = [
        ("fiction", "Fiction"),
        ("non_fiction", "Non-Fiction"),
        ("science", "Science"),
        ("technology", "Technology"),
        ("history", "History"),
        ("biography", "Biography"),
        ("fantasy", "Fantasy"),
        ("mystery", "Mystery"),
        ("romance", "Romance"),
        ("other", "Other"),
    ]
    
    title = models.CharField(max_length=255)
    isbn = models.CharField(max_length=15, unique=True)
    category = models.CharField(max_length=100, choices=CATEGORY_CHOICES, default="other")
    available = models.BooleanField(default=True)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name="books")
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.title} ({self.isbn})"
    
    class Meta:
        ordering = ["title"]
        
class BookImage(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='image')
    image = CloudinaryField('image', validators=[validate_file_size])
        
