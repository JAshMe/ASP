"""
This module will consist of all the Forms used in Accounts App
"""

from django.forms import *
from .models import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model


class UserForm(UserCreationForm):
    """
    This form will be responsible for Basic User Credentials
    """

    class Meta:
        model = get_user_model()
        fields = ['username', 'first_name', 'last_name', 'password1', 'password2', 'email']


class StudProfileForm(ModelForm):
    """
    This is the form which will be used for Student Profile Model
    """

    class Meta:
        model = StudentProfile
        fields = ['prog', 'bra', 'sem']


class TeacherProfileForm(ModelForm):
    """
    This is form which will be used for Teacher Profile Model
    """

    class Meta:
        model = TeacherProfile
        fields = ['bio', 'dept']









