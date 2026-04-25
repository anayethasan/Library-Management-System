from rest_framework import serializers
from borrow.models import BorrowRecord
from django.utils import timezone

class BorrowRecordSerializer(serializers.ModelSerializer):
    """List/Retrieve - To show all borrow records"""
    book_title = serializers.CharField(source='book.title', read_only=True)
    member_email = serializers.CharField(source='member.user.email', read_only=True)
    
    is_overdue = serializers.SerializerMethodField()
    late_fee = serializers.SerializerMethodField()
    
    class Meta:
        model = BorrowRecord
        fields = [
            'id', 'member_email', 'book', 'book_title',
            'borrow_date', 'due_date', 'return_date',
            'status', 'late_fee_charged', 'is_overdue', 'late_fee'
        ]
    read_only_fields = ['id', 'borrow_date', 'return_date', 'status', 'late_fee_charged']
    
    def get_is_overdue(self, obj):
        return obj.is_overdue()
    
    def get_late_fee(self, obj):
        return obj.late_fee()
    
class CreateBorrowSerializer(serializers.Serializer):
    """POST/api/borrow - that means do books borrow"""    
    book = serializers.IntegerField()
    due_date = serializers.DateField()
    
class ReturnBookSerializer(serializers.Serializer):
    """POST/api/borrow/<id>/return/ - do return book"""
    pass