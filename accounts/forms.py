"""
This module will consist of all the Forms used in Accounts App
"""

from django.forms import *
from .models import *
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth import get_user_model
from .form_funcs import *


class LoginForm(AuthenticationForm):
    """
    Form for login
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        update_all_inputs(self.fields, 'class', 'form-control')


class UserForm(UserCreationForm):
    """
    This form will be responsible for Basic User Credentials
    """

    class Meta:
        model = get_user_model()
        fields = ['username', 'first_name', 'last_name', 'password1', 'password2', 'email']

    def __init__(self, *args, **kwargs):
        """
        To customize the widgets
        """
        super().__init__(*args, **kwargs)

        update_all_inputs(self.fields, 'class', 'form-control')

        update_attr(self.fields['username'], 'class', 'form-control form-control-lg')


class StudProfileForm(ModelForm):
    """
    This is the form which will be used for Student Profile Model
    """

    class Meta:
        model = StudentProfile
        fields = ['prog', 'bra', 'sem']

    def __init__(self, *args, **kwargs):
        """
        To customize widgets
        """
        super().__init__(*args, **kwargs)

        update_all_inputs(self.fields, 'class', 'form-control')


class TeacherProfileForm(ModelForm):
    """
    This is form which will be used for Teacher Profile Model
    """

    class Meta:
        model = TeacherProfile
        fields = ['bio', 'dept']

    def __init__(self, *args, **kwargs):
        """
        To customize widgets
        """
        super().__init__(*args, **kwargs)

        update_all_inputs(self.fields, 'class', 'form-control')
        update_attr(self.fields['bio'], 'cols', 10)
        update_attr(self.fields['bio'], 'rows', 3)









