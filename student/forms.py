"""
Forms for Campus Pulse application.
Handles form rendering and validation for all modules.
"""
from django import forms
from .models import Student, Feedback


class StudentForm(forms.ModelForm):
    """Form for creating and updating student profile."""
    class Meta:
        model = Student
        fields = [
            'roll_number', 'register_number', 'student_name', 'email',
            'phone_number', 'department', 'year_semester', 'section',
            'date_of_birth', 'address', 'student_photo'
        ]
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
            'address': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Enter your address'}),
        }


class FeedbackForm(forms.ModelForm):
    """Form for submitting feedback."""
    class Meta:
        model = Feedback
        fields = ['subject', 'message']
        widgets = {
            'subject': forms.TextInput(attrs={'placeholder': 'Enter feedback subject'}),
            'message': forms.Textarea(attrs={'rows': 5, 'placeholder': 'Write your feedback here...'}),
        }


class PaymentForm(forms.Form):
    """Form for making fee payments."""
    amount = forms.DecimalField(
        max_digits=10, decimal_places=2,
        min_value=1,
        widget=forms.NumberInput(attrs={'placeholder': 'Enter amount to pay'})
    )
