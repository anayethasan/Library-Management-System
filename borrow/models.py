from django.db import models
from django.utils import timezone
from django.conf import settings
from books.models import Book
from member.models import Member

LATE_FEE_PER_DAY = 20

class BorrowRecord(models.Model):
    STATUS_CHOICES = [
        ("borrowed", "Borrowed"),
        ("returned", "Returned"),
    ]
    
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="borrow_records")
    member = models.ForeignKey(Member, on_delete=models.CASCADE, related_name="borrow_records")
    borrow_date = models.DateTimeField(auto_now_add=True)
    due_date = models.DateField()
    
    return_date = models.DateTimeField(blank=True, null=True)
    status = models.CharField(max_length=25, choices=STATUS_CHOICES, default="borrowed")
    
    late_fee_charged = models.PositiveIntegerField(default=0)
    
    def is_overdue(self):
        if self.status == 'borrowed':
            return timezone.now().date() > self.due_date
        return False
    
    def calculate_late_fee(self):
        if self.is_overdue():
            overdue_days = (timezone.now().date() - self.due_date).days
            return overdue_days * LATE_FEE_PER_DAY
        return 0
    
    def __str__(self):
        return f"{self.member.user.email} → {self.book.title} [{self.status}]"
    
    class Meta:
        ordering = ["-borrow_date"]
        unique_together = [["member", "book", "status"]]