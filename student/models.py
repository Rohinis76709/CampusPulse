"""
Models for Campus Pulse application.

Models:
  - Student: Stores student profile information
  - Academic: Stores marks for 5 subjects with auto-calculated total, percentage, grade, result
  - Attendance: Stores attendance records with auto-calculated percentage and status
  - Fee: Stores fee details with total, paid, and balance amounts
  - PaymentHistory: Stores payment transaction history
  - Feedback: Stores student feedback submissions
"""

from django.db import models
from django.contrib.auth.models import User


class Student(models.Model):
    """
    Student profile model.
    Linked to Django's built-in User model for authentication.
    Stores all personal and academic profile information.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    roll_number = models.CharField(max_length=20, unique=True)
    register_number = models.CharField(max_length=20, unique=True)
    student_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone_number = models.CharField(max_length=15)
    department = models.CharField(max_length=100)
    year_semester = models.CharField(max_length=20)  # e.g., "2nd Year / 3rd Semester"
    section = models.CharField(max_length=10)
    date_of_birth = models.DateField()
    address = models.TextField()
    student_photo = models.ImageField(upload_to='student_photos/', blank=True, null=True)

    def __str__(self):
        return f"{self.roll_number} - {self.student_name}"


class Academic(models.Model):
    """
    Academic marks model.
    Stores marks for 5 subjects and auto-calculates:
    - total_marks: Sum of all subject marks
    - percentage: (total_marks / 500) * 100
    - grade: A/B/C/D/F based on percentage
    - result: Pass/Fail based on percentage (>= 35)
    """
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='academics')
    semester = models.CharField(max_length=20)

    # Marks for 5 subjects (out of 100 each)
    subject1_name = models.CharField(max_length=100, default='Subject 1')
    subject1_marks = models.FloatField()
    subject2_name = models.CharField(max_length=100, default='Subject 2')
    subject2_marks = models.FloatField()
    subject3_name = models.CharField(max_length=100, default='Subject 3')
    subject3_marks = models.FloatField()
    subject4_name = models.CharField(max_length=100, default='Subject 4')
    subject4_marks = models.FloatField()
    subject5_name = models.CharField(max_length=100, default='Subject 5')
    subject5_marks = models.FloatField()

    # Auto-calculated fields
    total_marks = models.FloatField(editable=False, default=0)
    percentage = models.FloatField(editable=False, default=0)
    grade = models.CharField(max_length=2, editable=False, default='F')
    result = models.CharField(max_length=10, editable=False, default='Fail')

    def calculate_results(self):
        """Calculate total, percentage, grade, and result from subject marks."""
        self.total_marks = (
            self.subject1_marks + self.subject2_marks + self.subject3_marks +
            self.subject4_marks + self.subject5_marks
        )
        self.percentage = (self.total_marks / 500) * 100

        if self.percentage >= 90:
            self.grade = 'A+'
        elif self.percentage >= 80:
            self.grade = 'A'
        elif self.percentage >= 70:
            self.grade = 'B+'
        elif self.percentage >= 60:
            self.grade = 'B'
        elif self.percentage >= 50:
            self.grade = 'C'
        elif self.percentage >= 35:
            self.grade = 'D'
        else:
            self.grade = 'F'

        self.result = 'Pass' if self.percentage >= 35 else 'Fail'

    def save(self, *args, **kwargs):
        """Override save to auto-calculate before persisting."""
        self.calculate_results()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.student.roll_number} - Semester {self.semester}"


class Attendance(models.Model):
    """
    Attendance model.
    Stores total classes, attended classes, and absent classes.
    Auto-calculates:
    - percentage: (attended / total) * 100
    - status: 'Eligible' if >= 75%, 'Shortage' otherwise
    """
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='attendance_records')
    semester = models.CharField(max_length=20)
    subject = models.CharField(max_length=100)

    total_classes = models.IntegerField(default=0)
    attended_classes = models.IntegerField(default=0)

    @property
    def absent_classes(self):
        """Calculate absent classes as total - attended."""
        return self.total_classes - self.attended_classes

    @property
    def percentage(self):
        """Calculate attendance percentage."""
        if self.total_classes > 0:
            return round((self.attended_classes / self.total_classes) * 100, 2)
        return 0.0

    @property
    def status(self):
        """Determine attendance status based on percentage."""
        if self.percentage >= 75:
            return 'Eligible'
        return 'Shortage'

    def __str__(self):
        return f"{self.student.roll_number} - {self.subject}"


class Fee(models.Model):
    """
    Fee model.
    Stores total fee, paid fee, and auto-calculates balance fee.
    """
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='fees')
    semester = models.CharField(max_length=20)
    fee_type = models.CharField(max_length=100, default='Tuition Fee')
    total_fee = models.DecimalField(max_digits=10, decimal_places=2)
    paid_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    @property
    def balance_fee(self):
        """Calculate remaining balance."""
        return self.total_fee - self.paid_fee

    def __str__(self):
        return f"{self.student.roll_number} - {self.fee_type}"


class PaymentHistory(models.Model):
    """
    Payment history model.
    Records each payment transaction with date, amount, and remaining balance.
    """
    fee = models.ForeignKey(Fee, on_delete=models.CASCADE, related_name='payments')
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='payments')
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2)
    remaining_balance = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.roll_number} - ₹{self.amount_paid} on {self.payment_date.strftime('%d-%m-%Y')}"

    class Meta:
        ordering = ['-payment_date']


class Feedback(models.Model):
    """
    Feedback model.
    Stores student feedback with subject, message, and submission date.
    """
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='feedbacks')
    subject = models.CharField(max_length=200)
    message = models.TextField()
    submitted_date = models.DateTimeField(auto_now_add=True)
    is_resolved = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.student.roll_number} - {self.subject}"

    class Meta:
        ordering = ['-submitted_date']
