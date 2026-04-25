from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied, NotFound
from rest_framework import status
from books.models import Book
from borrow.models import BorrowRecord
from borrow.serializers import BorrowRecordSerializer, CreateBorrowSerializer
from borrow.services import BorrowService


class BorrowRecordViewSet(ModelViewSet):
    """
    GET/api/borrow/— him self or if admin you can see all borrow list 
    POST/api/borrow/— do borrow book
    GET/api/borrow/<id>/— specific record
    POST/api/borrow/<id>/return/  — do return book base on this id
    DELETE /api/borrow/<id>/— only for Librarian/admin
    """
    permission_classes = [IsAuthenticated]
    http_method_names = ['get', 'post', 'delete']

    def get_queryset(self):
        user = self.request.user
        qs = BorrowRecord.objects.select_related('member__user', 'book')

        if user.is_staff:
            return qs.all()
        return qs.filter(member__user=user)

    def get_serializer_class(self):
        if self.request.method == 'POST' and self.action == 'create':
            return CreateBorrowSerializer
        return BorrowRecordSerializer

    def create(self, request, *args, **kwargs):
        serializer = CreateBorrowSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            member = request.user.member_profile
        except Exception:
            raise PermissionDenied({"detail": "You must be a registered member to borrow books."})

        try:
            book = Book.objects.get(pk=serializer.validated_data['book'])
        except Book.DoesNotExist:
            raise NotFound({"detail": "Book not found."})

        record = BorrowService.borrow_book(
            member=member,
            book=book,
            due_date=serializer.validated_data['due_date'],
        )
        return Response(BorrowRecordSerializer(record).data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['post'], url_path='return')
    def return_book(self, request, pk=None):
        """POST /api/borrow/<id>/return/"""
        try:
            member = request.user.member_profile
        except Exception:
            raise PermissionDenied({"detail": "You must be a registered member."})

        try:
            # Member only can do self record return 
            if request.user.is_staff:
                record = BorrowRecord.objects.get(pk=pk)
            else:
                record = BorrowRecord.objects.get(pk=pk, member=member)
        except BorrowRecord.DoesNotExist:
            raise NotFound({"detail": "Borrow record not found."})

        result = BorrowService.return_book(record)
        return Response(result, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        if not request.user.is_staff:
            raise PermissionDenied("Only librarians can delete borrow records.")
        return super().destroy(request, *args, **kwargs)