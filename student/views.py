"""
Views for Campus Pulse application.
Handles all business logic for profile, academics, attendance, fee, and feedback modules.
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib import messages
from .models import Student, Academic, Attendance, Fee, PaymentHistory, Feedback
from .forms import StudentForm, FeedbackForm, PaymentForm


def home(request):
    """Render the home page with college name and feature cards."""
    context = {
        'college_name': 'Mother Teresa Institution',
        'campus_name': 'Campus Pulse',
    }
    return render(request, 'student/home.html', context)


def login_view(request):
    """Handle user login with username and password."""
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, 'Login successful!')
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'student/login.html', {'form': form})


def register_view(request):
    """Handle new user registration. Creates User and Student profile."""
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Create a basic student profile linked to the user
            Student.objects.create(
                user=user,
                roll_number=f'ROLL{user.id:04d}',
                register_number=f'REG{user.id:04d}',
                student_name=user.username,
                email=f'{user.username}@campus.edu',
                phone_number='',
                department='Not Assigned',
                year_semester='1st Year / 1st Semester',
                section='A',
                date_of_birth='2000-01-01',
                address='Not provided',
            )
            messages.success(request, 'Registration successful! Please login.')
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'student/register.html', {'form': form})


def logout_view(request):
    """Log out the current user and redirect to home."""
    logout(request)
    messages.success(request, 'You have been logged out.')
    return redirect('home')


@login_required
def profile(request):
    """Display and update student profile."""
    try:
        student = Student.objects.get(user=request.user)
    except Student.DoesNotExist:
        student = None

    if request.method == 'POST':
        form = StudentForm(request.POST, request.FILES, instance=student)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user
            if not student:
                profile.roll_number = f'ROLL{request.user.id:04d}'
                profile.register_number = f'REG{request.user.id:04d}'
            profile.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('profile')
    else:
        form = StudentForm(instance=student)

    return render(request, 'student/profile.html', {
        'form': form,
        'student': student,
    })


@login_required
def academics(request):
    """Display academic marks with auto-calculated total, percentage, grade, and result."""
    try:
        student = Student.objects.get(user=request.user)
        academics = Academic.objects.filter(student=student)
    except Student.DoesNotExist:
        academics = []
    return render(request, 'student/academics.html', {'academics': academics})


@login_required
def attendance(request):
    """Display attendance records for the logged-in student."""
    try:
        student = Student.objects.get(user=request.user)
        records = Attendance.objects.filter(student=student)
    except Student.DoesNotExist:
        records = []
    return render(request, 'student/attendance.html', {'records': records})


@login_required
def fee(request):
    """Display fee details and payment form for the student."""
    try:
        student = Student.objects.get(user=request.user)
        fees = Fee.objects.filter(student=student)
    except Student.DoesNotExist:
        fees = []
    return render(request, 'student/fee.html', {'fees': fees})


@login_required
def make_payment(request, fee_id):
    """Handle fee payment. Updates paid fee, balance fee, and creates payment history."""
    fee_obj = get_object_or_404(Fee, id=fee_id, student__user=request.user)

    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            amount = form.cleaned_data['amount']
            if amount > fee_obj.balance_fee:
                messages.error(
                    request,
                    f'Payment amount (₹{amount}) exceeds balance fee (₹{fee_obj.balance_fee}).'
                )
                return redirect('fee')

            # Update fee record
            fee_obj.paid_fee += amount
            fee_obj.save()

            # Create payment history record
            PaymentHistory.objects.create(
                fee=fee_obj,
                student=fee_obj.student,
                amount_paid=amount,
                remaining_balance=fee_obj.balance_fee,
            )

            messages.success(request, f'Payment of ₹{amount} successful!')
            return redirect('payment_history')
    else:
        form = PaymentForm()

    return render(request, 'student/make_payment.html', {
        'form': form,
        'fee': fee_obj,
    })


@login_required
def payment_history(request):
    """Display payment history for the logged-in student."""
    try:
        student = Student.objects.get(user=request.user)
        payments = PaymentHistory.objects.filter(student=student)
    except Student.DoesNotExist:
        payments = []
    return render(request, 'student/payment_history.html', {'payments': payments})


def feedback(request):
    """Handle feedback submission and display previous feedback."""
    try:
        student = Student.objects.get(user=request.user)
    except Student.DoesNotExist:
        student = None

    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            feedback = form.save(commit=False)
            feedback.student = student
            feedback.save()
            messages.success(request, 'Feedback submitted successfully!')
            return redirect('feedback')
    else:
        form = FeedbackForm()

    feedbacks = Feedback.objects.filter(student=student) if student else []
    return render(request, 'student/feedback.html', {
        'form': form,
        'feedbacks': feedbacks,
    })
