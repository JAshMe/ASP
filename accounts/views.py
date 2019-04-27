from django.shortcuts import render, redirect, reverse
from django.views import View
from django.http import HttpResponse
import abc

from django.contrib.auth.views import LoginView, TemplateView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from django.views.generic import FormView
from pprint import pprint as pp
from .mixins import *
from .forms import *
from .models import *

# Create your views here.


class LoginPageView(LoginView):

    template_name = "accounts/login.html"
    redirect_authenticated_user = True
    form_class = LoginForm

    def get_context_data(self, **kwargs):
        """
        Extra context data for template
        :param kwargs: Keyword Args
        :return: Dict
        """
        context_data = super().get_context_data()

        #  if coming from signup page
        try:
            if self.request.session['acc_created'] == 1:
                context_data['acc_created'] = 1
                pp(context_data)
                self.request.session['acc_created'] = 0
                pp(context_data)
        except KeyError:
            pass

        # if coming from logout page
        try:
            if self.request.session['logout'] == 1:
                pp(context_data)
                context_data['logout'] = 1
                self.request.session['logout'] = 0
                pp(context_data)
        except KeyError:
            pass

        return context_data

    def form_valid(self, form):
        """
        To set the type of user in session
        :param form: AuthenticationForm
        :return: HTTPResponse
        """
        response = super().form_valid(form)

        user = self.request.user
        if user.is_stud:
            self.request.session['is_stud'] = True
        else:
            self.request.session['is_stud'] = False

        return response


class StudSignUp(View):
    """
    This view will be used to display SignUp Form for Student
    Which will consist of UserForm and Profile Form
    """
    success_url = settings.LOGIN_URL
    template_name = "accounts/signup.html"

    def get(self, request):
        """
        This method will display blank forms of User Credentials and Student Profile
        :param request: HTTP Request
        :return: HTTP Response
        """
        context = {
            'is_stud': True,
            'userform': UserForm(),
            'studform': StudProfileForm()
        }

        return render(request, template_name=self.template_name, context=context)

    def post(self, request):
        """
        This method will the posted form data of both the forms
        :param request: HTTP Request
        :return: HTTP Response
        """

        userform = UserForm(request.POST)
        studform = StudProfileForm(request.POST)

        if userform.is_valid() and studform.is_valid():  # save the info
            user = userform.save(commit=False)
            user.is_stud = True
            user.save()
            user.refresh_from_db()  # to resolve sync problems with profile model

            # storing its profile
            user.studentprofile.prog = studform.cleaned_data['prog']
            user.studentprofile.sem = studform.cleaned_data['sem']
            user.studentprofile.bra = studform.cleaned_data['bra']

            user.save()

            # redirect to login page
            request.session['acc_created'] = 1
            return redirect(self.success_url)

        else:  # one of them is invalid, so send them back for correction displaying the errors
            context = {
                'is_stud': True,
                'userform': userform,
                'studform': studform,

            }
            return render(request, template_name=self.template_name, context=context)


class TeacherSignUp(View):

    template_name = 'accounts/signup.html'
    success_url = settings.LOGIN_URL

    def get(self, request):
        """
        This method will display blank forms of User Credentials and Teacher Profile
        :param request: HTTP Request
        :return: HTTP Response
        """
        context = {
            'is_stud': False,
            'userform': UserForm(),
            'teacherform': TeacherProfileForm()
        }

        return render(request, template_name=self.template_name, context=context)

    def post(self, request):
        """
        This method will the posted form data of both the forms
        :param request: HTTP Request
        :return: HTTP Response
        """

        userform = UserForm(request.POST)
        teacherform = TeacherProfileForm(request.POST)

        if userform.is_valid() and teacherform.is_valid():  # save the info
            user = userform.save(commit=False)
            user.is_stud = False
            user.save()
            user.refresh_from_db()  # to resolve sync problems with profile model

            # storing its profile
            user.teacherprofile.bio = teacherform.cleaned_data['bio']
            user.teacherprofile.dept = teacherform.cleaned_data['dept']

            user.save()

            # redirect to login page
            request.session['acc_created'] = 1
            return redirect(self.success_url)

        else:  # one of them is invalid, so send them back for correction displaying the errors
            context = {
                'is_stud': False,
                'userform': userform,
                'studform': teacherform,

            }
            return render(request, template_name=self.template_name, context=context)


#  ------------------------------- Below Views Accessible only after Login --------------------------------------


class ChooseDashboardView(LoginRequiredMixin, View):
    """
    This view will choose the appropriate Dashboard for user depending on its role
    """
    def get(self, request):

        if self.request.session['is_stud']:
            return redirect(to=reverse("accounts:stud_dash"))
        else:
            return redirect(to=reverse("accounts:teacher_dash"))


class DashboardView(TemplateView):

    template_name = "accounts/login.html"

    def get_context_data(self, **kwargs):
        """
        To fill the context data
        :param kwargs: Keyword Arguments
        :return: Context Data dict
        """
        context_data = super().get_context_data()
        context_data['user'] = self.request.user

        return context_data


class StudDashboardView(StudLoginRequiredMixin, DashboardView):
    """
        This is Student Dashboard View
    """

    template_name = "accounts/stud_dash.html"

    def test_func(self):
        return self.request.session['is_stud']


class TeacherDashboardView(TeacherLoginRequiredMixin, DashboardView):
    """
    This is the Teacher's Dashboard View
    """

    template_name = "accounts/teacher_dash.html"

    def test_func(self):
        return not self.request.session['is_stud']


class LogOutView(LogoutView):
    """
    View to log user out
    It will logout and redirect to settings.LOGOUT_REDIRECT_URL
    """

    def get(self, request, *args, **kwargs):
        """
        Overriding to set the logout session variable
        """

        print("Hello")
        self.request.session['logout'] = 1

        return super().get(request, *args, **kwargs)



