from django.forms.models import ModelForm
from django.forms.widgets import *
from django.forms import Form, ChoiceField, ValidationError, CharField
from .models import Assignment, Environment
from accounts.form_funcs import *


class AssignmentForm(ModelForm):
    """
    This form will be used to Create and Edit the Assignments of a Student
    """
    class Meta:
        model = Assignment
        fields = ['title', 'desc', 'env', 'assign_code', 'run_command', ]

    def get_non_control_inputs(self):
        """
        All the non-selects, non-texts, non-passes, non-textareas
        :return: Dict of Fields
        """
        return {
            'assign_code': self.fields['assign_code']
        }

    def __init__(self, *args, **kwargs):
        """
        To customize widgets
        """
        super().__init__(*args, **kwargs)
        update_all_inputs(self.fields, 'class', 'form-control', self.get_non_control_inputs())

        update_attr(self.fields['assign_code'], 'class', 'custom-file-input')


class EnvSelectForm(Form):
    """
    This form will be used for Environment Selection
    """

    env_id = ChoiceField(
        label="Environment",
        choices=Environment.ENVIRONMENT_CHOICES,
    )

    def __init__(self, *args, **kwargs):
        """
        To customize widgets
        """
        super().__init__(*args, **kwargs)
        update_attr(self.fields['env_id'], 'class', 'form-control')


    def clean_env_id(self):  # clean_fieldname
        """
        Method to validate whether the env_id chosen exists in DB or not
        :return: None and Raise ValidationError if Doesn't Exist
        """
        env_id = self.cleaned_data['env_id']
        try:
            env = Environment.objects.get(pk=env_id)
        except Environment.DoesNotExist:
            raise ValidationError("Selected Environment Not Present")

        return env_id


class AssignSelectForm(Form):
    """
    This form will be used for Assignment Selection
    """

    assign_id = CharField(
        label="Assignment ID",
        max_length=10,
        min_length=10,
        required=True,
    )

    def clean_assign_id(self):
        """
        Need to have ID which exists in the Database
        :return: Cleaned ID
        """

        assign_id = self.cleaned_data['assign_id']
        try:
            assign = Assignment.objects.get(assign_id=assign_id)
        except Assignment.DoesNotExist:
            raise ValidationError("Please enter Valid Assignment ID!")

        return assign_id



