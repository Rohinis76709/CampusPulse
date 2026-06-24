"""
Management command to insert sample data for testing.
Run: python manage.py insert_sample_data
Creates a test student, academic records, attendance, fees, and feedback.
"""
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from student.models import Student, Academic, Attendance, Fee, Feedback


class Command(BaseCommand):
    help = 'Inserts sample data for testing Campus Pulse'

    def handle(self, *args, **kwargs):
        # Create test user if not exists
        user, created = User.objects.get_or_create(
            username='student1',
            defaults={'email': 'student1@campus.edu'}
        )
        if created:
            user.set_password('student123')
            user.save()
            self.stdout.write(self.style.SUCCESS('Created user: student1 / student123'))
        else:
            self.stdout.write('User student1 already exists')

        # Create student profile
        student, created = Student.objects.get_or_create(
            roll_number='ROLL0001',
            defaults={
                'user': user,
                'register_number': 'REG2024001',
                'student_name': 'John Doe',
                'email': 'john@campus.edu',
                'phone_number': '9876543210',
                'department': 'Computer Science',
                'year_semester': '2nd Year / 3rd Semester',
                'section': 'A',
                'date_of_birth': '2003-05-15',
                'address': '123 Main Street, City',
            }
        )
        if created:
            self.stdout.write(self.style.SUCCESS('Created student: John Doe'))
        else:
            self.stdout.write('Student already exists')

        # Create academic records
        acad, created = Academic.objects.get_or_create(
            student=student,
            semester='3rd Semester',
            defaults={
                'subject1_name': 'Data Structures',
                'subject1_marks': 85,
                'subject2_name': 'Database Systems',
                'subject2_marks': 78,
                'subject3_name': 'Computer Networks',
                'subject3_marks': 92,
                'subject4_name': 'Operating Systems',
                'subject4_marks': 74,
                'subject5_name': 'Software Engineering',
                'subject5_marks': 88,
            }
        )
        if created:
            self.stdout.write(self.style.SUCCESS(
                f'Created academic record - Total: {acad.total_marks}, '
                f'Percentage: {acad.percentage:.2f}%, Grade: {acad.grade}, Result: {acad.result}'
            ))

        # Create attendance records
        subjects_data = [
            ('Data Structures', 30, 27),
            ('Database Systems', 30, 24),
            ('Computer Networks', 30, 28),
            ('Operating Systems', 30, 20),
            ('Software Engineering', 30, 26),
        ]
        for subject, total, attended in subjects_data:
            att, created = Attendance.objects.get_or_create(
                student=student,
                semester='3rd Semester',
                subject=subject,
                defaults={
                    'total_classes': total,
                    'attended_classes': attended,
                }
            )
            if created:
                self.stdout.write(self.style.SUCCESS(
                    f'Created attendance for {subject} - {att.percentage}% ({att.status})'
                ))

        # Create fee records
        fee, created = Fee.objects.get_or_create(
            student=student,
            semester='3rd Semester',
            fee_type='Tuition Fee',
            defaults={
                'total_fee': 50000,
                'paid_fee': 25000,
            }
        )
        if created:
            self.stdout.write(self.style.SUCCESS(
                f'Created fee record - Total: Rs.{fee.total_fee}, Paid: Rs.{fee.paid_fee}, Balance: Rs.{fee.balance_fee}'
            ))

        # Create feedback
        fb, created = Feedback.objects.get_or_create(
            student=student,
            subject='Library Hours',
            defaults={
                'message': 'The library should be open until 8 PM for students who want to study late.',
            }
        )
        if created:
            self.stdout.write(self.style.SUCCESS('Created feedback: Library Hours'))

        self.stdout.write(self.style.SUCCESS('\nSample data insertion completed!'))
        self.stdout.write(self.style.SUCCESS('Login with username: student1, password: student123'))
