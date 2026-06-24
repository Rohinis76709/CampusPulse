from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from student.models import Student, Academic, Attendance, Fee, PaymentHistory, Feedback
from decimal import Decimal
from datetime import date


class Command(BaseCommand):
    help = 'Seed sample data for Campus Pulse'

    def handle(self, *args, **options):
        user, created = User.objects.get_or_create(
            username='student1',
            defaults={
                'email': 'student1@campus.edu',
                'is_staff': True,
            }
        )
        if created:
            user.set_password('password123')
            user.save()
            self.stdout.write(self.style.SUCCESS('Created user: student1'))

        student, _ = Student.objects.get_or_create(
            user=user,
            defaults={
                'roll_number': 'ROLL0001',
                'register_number': 'REG0001',
                'student_name': 'Rohini Sharma',
                'email': 'student1@campus.edu',
                'phone_number': '9876543210',
                'department': 'Computer Science',
                'year_semester': '2nd Year / 3rd Semester',
                'section': 'A',
                'date_of_birth': date(2004, 5, 15),
                'address': '123, Main Street, Pune - 411001',
            }
        )
        self.stdout.write(self.style.SUCCESS(f'Student: {student.student_name}'))

        acad, _ = Academic.objects.get_or_create(
            student=student,
            semester='3rd Semester',
            defaults={
                'subject1_name': 'Data Structures',
                'subject1_marks': 85,
                'subject2_name': 'Database Systems',
                'subject2_marks': 78,
                'subject3_name': 'Operating Systems',
                'subject3_marks': 92,
                'subject4_name': 'Computer Networks',
                'subject4_marks': 74,
                'subject5_name': 'Software Engineering',
                'subject5_marks': 88,
            }
        )
        self.stdout.write(self.style.SUCCESS(f'Academics: {acad.total_marks}/500 ({acad.percentage}%) - {acad.grade}'))

        Attendance.objects.get_or_create(
            student=student,
            semester='3rd Semester',
            subject='Data Structures',
            defaults={'total_classes': 40, 'attended_classes': 36}
        )
        Attendance.objects.get_or_create(
            student=student,
            semester='3rd Semester',
            subject='Database Systems',
            defaults={'total_classes': 35, 'attended_classes': 28}
        )
        Attendance.objects.get_or_create(
            student=student,
            semester='3rd Semester',
            subject='Operating Systems',
            defaults={'total_classes': 38, 'attended_classes': 32}
        )
        self.stdout.write(self.style.SUCCESS('Attendance records created'))

        fee, _ = Fee.objects.get_or_create(
            student=student,
            semester='3rd Semester',
            fee_type='Tuition Fee',
            defaults={'total_fee': Decimal('45000.00'), 'paid_fee': Decimal('25000.00')}
        )
        self.stdout.write(self.style.SUCCESS(f'Fee: Rs.{fee.total_fee} (Paid: Rs.{fee.paid_fee}, Balance: Rs.{fee.balance_fee})'))

        self.stdout.write(self.style.SUCCESS('\nSample data inserted successfully!'))
        self.stdout.write(self.style.SUCCESS('Login with username: student1, password: password123'))
