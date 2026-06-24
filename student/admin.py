"""
Admin configuration for Campus Pulse.
Registers all models in the Django admin panel for CRUD operations.
"""
from django.contrib import admin
from .models import Student, Academic, Attendance, Fee, PaymentHistory, Feedback


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ['roll_number', 'register_number', 'student_name', 'department', 'year_semester']
    search_fields = ['roll_number', 'register_number', 'student_name']
    list_filter = ['department', 'year_semester']


@admin.register(Academic)
class AcademicAdmin(admin.ModelAdmin):
    list_display = ['student', 'semester', 'total_marks', 'percentage', 'grade', 'result']
    list_filter = ['semester', 'result']


@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ['student', 'subject', 'total_classes', 'attended_classes', 'percentage', 'status']
    list_filter = ['semester']


@admin.register(Fee)
class FeeAdmin(admin.ModelAdmin):
    list_display = ['student', 'fee_type', 'total_fee', 'paid_fee', 'balance_fee']
    list_filter = ['semester']


@admin.register(PaymentHistory)
class PaymentHistoryAdmin(admin.ModelAdmin):
    list_display = ['student', 'amount_paid', 'remaining_balance', 'payment_date']
    readonly_fields = ['payment_date']


@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ['student', 'subject', 'submitted_date', 'is_resolved']
    list_filter = ['is_resolved']
