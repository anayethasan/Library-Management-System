from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser
from books.models import Book
from member.models import Member
from borrow.models import BorrowRecord
from books.serializers import BookSerializer
from member.serializers import MemberSerializer
from borrow.serializers import BorrowRecordSerializer


class TotalBooksView(APIView):
    
    """
    GET /api/dashboard/total-books/
    Returns total book count and full list of all books in the library.
    Restricted to Librarians/Admins only.
    """
    permission_classes = [IsAdminUser]
 
    def get(self, request):
        books = Book.objects.select_related('author').prefetch_related('images').all()
        return Response({
            "total_books": books.count(),
            "books": BookSerializer(books, many=True, context={'request': request}).data
        })


class TotalMembersView(APIView):
    """
    GET /api/dashboard/total-members/
    Returns total member count and full list of registered members.
    Restricted to Librarians/Admins only.
    """
    permission_classes = [IsAdminUser]
 
    def get(self, request):
        members = Member.objects.select_related('user').prefetch_related('borrow_records').all()
        return Response({
            "total_members": members.count(),
            "members": MemberSerializer(members, many=True, context={'request': request}).data
        })


class BorrowedBooksView(APIView):
    """
    GET /api/dashboard/borrowed-books/
    Returns count of currently borrowed books, overdue count,
    and the full list of active borrow records.
    Restricted to Librarians/Admins only.
    """
    permission_classes = [IsAdminUser]
 
    def get(self, request):
        borrowed = BorrowRecord.objects.select_related('member__user', 'book').filter(status="borrowed")
        overdue = [r for r in borrowed if r.is_overdue()]
        return Response({
            "currently_borrowed": borrowed.count(),
            "overdue_count": len(overdue),
            "borrowed_list": BorrowRecordSerializer(borrowed, many=True, context={'request': request}).data
        })

class AvailableBooksView(APIView):
    """
    GET /api/dashboard/available-books/
    Returns count of available books and their full details.
    Restricted to Librarians/Admins only.
    """
    permission_classes = [IsAdminUser]
 
    def get(self, request):
        books = Book.objects.select_related('author').prefetch_related('images').filter(available=True)
        return Response({
            "available_books": books.count(),
            "books": BookSerializer(books, many=True, context={'request': request}).data
        })