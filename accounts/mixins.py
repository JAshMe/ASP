"""
This module will store all the custom Mixins
"""

from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin


class StudRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.session['is_stud']


class TeacherRequiredMixin(UserPassesTestMixin):

    def test_func(self):
        return not self.request.session['is_stud']


class StudLoginRequiredMixin(LoginRequiredMixin, StudRequiredMixin):
    pass


class TeacherLoginRequiredMixin(LoginRequiredMixin, TeacherRequiredMixin):

    pass


