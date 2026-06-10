"""Forms for homework management app."""

from django import forms
from .models import Homework, Submission, Subject


class HomeworkForm(forms.ModelForm):
    """Form for creating and editing homework assignments."""
    class Meta:
        model = Homework
        fields = ['title', 'description', 'subject', 'assigned_to', 'due_date', 'points', 'attachments']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'subject': forms.Select(attrs={'class': 'form-control'}),
            'assigned_to': forms.CheckboxSelectMultiple(),
            'due_date': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'points': forms.NumberInput(attrs={'class': 'form-control'}),
            'attachments': forms.FileInput(attrs={'class': 'form-control'}),
        }


class SubmissionForm(forms.ModelForm):
    """Form for submitting homework."""
    class Meta:
        model = Submission
        fields = ['submission_file']
        widgets = {
            'submission_file': forms.FileInput(attrs={'class': 'form-control'}),
        }


class GradeSubmissionForm(forms.ModelForm):
    """Form for grading submissions."""
    class Meta:
        model = Submission
        fields = ['score', 'feedback']
        widgets = {
            'score': forms.NumberInput(attrs={'class': 'form-control'}),
            'feedback': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }
