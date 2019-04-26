from django.shortcuts import render,reverse, redirect
from django.views import View
from django.views.generic import TemplateView, CreateView, FormView, DetailView
from .models import Assignment, Environment, VM
from django.http.response import FileResponse
from .forms import AssignmentForm, EnvSelectForm, AssignSelectForm
import time, math, random, subprocess
import hashlib
from .portscanner import get_free_port
from accounts.mixins import *
from django.http import HttpResponse
from ASP import settings


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

        ass = Assignment.objects.get(pk=pk)
        free_port = self.create_vm()

        self.deploy_stud_code(ass)

        web_shell_url = "http://127.0.0.1:" + str(free_port) + "/"
        return redirect(to=web_shell_url)

    def create_vm(self):
        """
        This method will create the VM for that using Vagrant Script
        :return: Port at which the Web Shell is running on VM
        """

        # getting required parameters for the script
        username = self.request.user.username
        free_port = str(self.get_port())

        cmd = "assignments/env/start-vm.sh -u %s -p %s" % (username, free_port)
        print("Running " + cmd + "....")

        # running shell script with above parameters
        subprocess.call(["cd assignments & pwd & " + cmd], shell=True)

        print("VM Created..")

        # inserting the new vm in the database
        self.store_new_vm(free_port)

        return free_port

    def deploy_stud_code(self, ass):
        """
        This method will deploy the student code in above created VM
        :return: None
        """

        # getting required parameters
        env_name = ass.env.env_id
        code_url = "http://127.0.0.1:8000/" + ass.assign_code.url

        code_url = "https://github.com/Abhey/SparkTestApp/archive/master.zip"

        run_command = ass.run_command

        run_command = "/spark/bin/spark-submit /code/SparkTestApp-master/SparkApp.py"
        username = self.request.user.username

        # getting the script
        script_url = ass.env.bash_file_url

        cmd = "%s -u %s -l %s -c \"%s\" -e %s" % (script_url, username, code_url, run_command, env_name)

        print("Running " + cmd + "....")

        # pass these parameters to above bash script and run it
        subprocess.call([cmd], shell=True)

    def get_port(self):
        """
        This method is used for getting port for the VM
        :return: Integer: Port
        """

        teacher = self.request.user

        try:
            # try to fetch port from existing model for the teacher
            vm = VM.objects.get(pk=teacher)
            return vm.port_used

        except VM.DoesNotExist:
            return get_free_port()  # else get a free port for that teacher

    def store_new_vm(self, port):
        """
        THis method will store new VM spawned, for that teacher
        :param port: THe port at which VM is running
        :return: None
        """

        new_vm = VM(self.request.user.username, port)

        print(self.request.user)

        new_vm.save()

        print("New VM inserted in the Database..")

        return




























