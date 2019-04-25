from django.shortcuts import render,reverse
from django.views.generic import TemplateView, CreateView
from .models import Assignment
from .forms import AssignmentForm


class IndexView(TemplateView):
    template_name = 'assignments/index.html'


class CreateAssignmentView(CreateView):
    """
    This assignment will store the new Assignment to Database
    """
    form_class = AssignmentForm
    template_name = "assignments/add_assign.html"
    success_url = 'assign_success'

    def form_valid(self, form):
        """
        This method called after after validation of the form
        :param form: The bound ModelForm
        :return: HTTPRedirectResponse
        """

        form.instance.user = self.request.user  # mapping user with the assignment
        return super().form_valid(form)


class AssignSuccessView(TemplateView):
    """
    View to display on Assignment Success
    """
    template_name = "assignments/assign_success.html"




