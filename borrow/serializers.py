from rest_framework import serializers
from books.models import BorrowRecord

class BorrowRecordSerializer(serializers.ModelSerializer):
    who_borrow = serializers.SerializerMethodField()
    
    class Meta:
        model = BorrowRecord
        fields = ['id', 'book', 'member', 'borrow_date', 'return_date', 'status', 'who_borrow']
    
    def get_who_borrow(self, obj):
        return obj.member.user.email