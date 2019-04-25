from django.shortcuts import render,reverse, redirect
from django.views import View
from django.views.generic import TemplateView, CreateView, FormView, DetailView
from .models import Assignment, Environment
from django.http.response import FileResponse
from .forms import AssignmentForm, EnvSelectForm, AssignSelectForm
import time, math, random, subprocess
import hashlib
from .portscanner import get_free_port
from accounts.mixins import *
from django.http import HttpResponse


class IndexView(TemplateView):
    template_name = 'assignments/index.html'


class CreateAssignmentView(StudLoginRequiredMixin, CreateView):
    """
    This assignment will store the new Assignment to Database
    """
    form_class = AssignmentForm
    template_name = "assignments/add_assign.html"
    success_url = 'success'

    def form_valid(self, form):
        """
        This method called after after validation of the form
        :param form: The bound ModelForm
        :return: HTTPRedirectResponse
        """

        form.instance.user = self.request.user  # mapping user with the assignment
        form.instance.assign_id = self.gen_unique_id(form.instance)
        self.request.session['assign_sub'] = form.instance.assign_id
        return super().form_valid(form)

    def gen_unique_id(self, ass_instance):
        """
        This method will generate a unique id for Every Assignment,
        which upon entering, will fetch the assignment and its details
        :param ass_instance: Assignment Instance
        :return: String
        """

        user_regno = str(ass_instance.user.username)
        curr_time = math.ceil(time.time())
        rand_no = random.randint(1, 1000000)

        enc_str = user_regno + str(curr_time) + str(rand_no)

        unique_id = hashlib.sha256(enc_str.encode()).hexdigest()
        unique_id = unique_id[:10]

        try:
            test_ass = Assignment.objects.get(assign_id=unique_id)
            return self.gen_unique_id(ass_instance)
        except Assignment.DoesNotExist:
            return unique_id


class AssignSuccessView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    """
    View to display on Assignment Success
    """
    template_name = "assignments/assign_success.html"

    def test_func(self):
        if 'assign_sub' in self.request.session:
            return True
        return False

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)

        assign_id = self.request.session['assign_sub']
        self.request.session.pop('assign_sub', None)

        assign = Assignment.objects.get(assign_id=assign_id)

        context_data['assign'] = assign

        return context_data


class EnvSelectView(LoginRequiredMixin, FormView):
    """
        View to enable downloading of Different Environments
    """
    template_name = "assignments/env_select.html"
    form_class = EnvSelectForm

    def form_valid(self, form):
        """
        After valid data has been POSTed, return resp file in the response
        :param form: EnvSelectForm
        :return: HTTPResponse
        """
        env_id = form.cleaned_data['env_id']
        env = Environment.objects.get(pk=env_id)

        file_to_download = env.bash_file_url

        # return this file for downloading
        return FileResponse(
            open(file_to_download, 'rb'),
            as_attachment=True,
        )


class AssignSelectView(TeacherLoginRequiredMixin, FormView):
    """
    This view will take the AssignID as input, to evaluate that assignment
    """

    template_name = "assignments/assign_select.html"
    form_class = AssignSelectForm

    def form_valid(self, form):
        """
        After Valid Assignment ID is posted, insert it to the session
        :param form: AssignSelectForm
        :return: HTTPResponse
        """

        self.request.session['curr_assign'] = form.cleaned_data['assign_id']

        return redirect(reverse("assignments:assign-detail", kwargs={'pk': form.cleaned_data['assign_id']}))


class AssignDetailView(TeacherLoginRequiredMixin, DetailView):

    """
    View to define details of an Assignment
    """

    model = Assignment
    template_name = "assignments/assign_eval.html"
    context_object_name = "assign"

# ---------Following View Will be used for Evaluation of the Uploaded Assignment------------


class EvalAssignView(TeacherLoginRequiredMixin, View):
    """
    View to Evaluate the Assignment
    """

    def get(self, request, pk):
        """
        :param request: HTTPRequest
        :param pk: Primary Key of the Assignment
        :return: HTTPResponse
        """

        self.create_vm()
        return HttpResponse("Evaluated")

    def create_vm(self):
        """
        This method will create the VM for that using Vagrant Script
        :return: None
        """

        # getting required parameters for the script
        username = self.request.user.username
        free_port = get_free_port()

        print(username + " " + str(free_port))






















