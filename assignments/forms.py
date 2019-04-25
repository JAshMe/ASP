from django.forms.models import ModelForm
from django.forms.widgets import *
from .models import Assignment


class AssignmentForm(ModelForm):
    """
    This form will be used to Create and Edit the Assignments of a Student
    """
    class Meta:
        model = Assignment
        fields = ['title', 'desc', 'env', 'assign_code', 'run_command', ]
        widgets = {
            'submission_time': DateTimeInput(attrs={
                'disabled': True
            })
        }
