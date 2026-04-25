from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser
from books.models import Book
from member.models import Member
from borrow.models import BorrowRecord


class TotalBooksView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        return Response({"total_books": Book.objects.count()})


class TotalMembersView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        return Response({"total_members": Member.objects.count()})


class BorrowedBooksView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        borrowed = BorrowRecord.objects.filter(status="borrowed")
        overdue = [r for r in borrowed if r.is_overdue()]
        return Response({
            "currently_borrowed": borrowed.count(),
            "overdue": len(overdue),
        })


class AvailableBooksView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        return Response({
            "available_books": Book.objects.filter(available=True).count()
        })