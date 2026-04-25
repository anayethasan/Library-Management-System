from django.db import transaction
from django.utils import timezone
from rest_framework.exceptions import ValidationError
from borrow.models import BorrowRecord

class BorrowService:
    
    @staticmethod
    def borrow_book(member, book, due_date):
        """Book borrow logic"""
        with transaction.atomic():
            #book available or not
            if not book.available:
                raise ValidationError({"detail": f'"{book.title}" is currently not available'})
            
            #before borrowed or not
            already_borrowed = BorrowRecord.objects.filter(member=member, book=book, status="borrowed").exists()
            
            if already_borrowed:
                raise ValidationError({"detail": "You have already borrowed this book."})
            
            #in future section due date available or not
            if due_date <= timezone.now().date():
                raise ValidationError({"detail": "Due date must be in the future."})
            
            #do Book unavailable
            book.available = False
            book.save()
            
            record = BorrowRecord.objects.create(
                member=member,
                book=book,
                due_date=due_date,
            )
            return record
        
        @staticmethod
        def return_book(borrow_record):
            """äll record for all books"""
            with transaction.atomic():
                if borrow_record.status == "returned":
                    raise ValidationError({"detail": "This book already has been returned."})
                
                late_fee = borrow_record.calculate_late_fee()
                
                #update Records
                borrow_record.status = "returned"
                borrow_record.return_date = timezone.now()
                borrow_record.late_fee_charged = late_fee
                borrow_record.save()
                
                #Available book again
                book = borrow_record.book
                book.available = True
                book.save()
                
                return {
                    "message": f'"{book.title}" returned successfully.',
                    "late_fee_charged": late_fee
                }
                