"""
URLs of Accounts App
"""

from django.urls import path, include
from .views import *

app_name = 'accounts'

urlpatterns = [
    path('login/', LoginPageView.as_view(), name='login'),
    path('signup/stud', StudSignUp.as_view(), name='stud_signup'),
    path('signup/teacher', TeacherSignUp.as_view(), name='teacher_signup'),
    path('dash/', ChooseDashboardView.as_view(), name='choose_dash'),
    path('dash/stud', StudDashboardView.as_view(), name='stud_dash'),
    path('dash/teacher', TeacherDashboardView.as_view(), name='teacher_dash'),
    path('logout', LogOutView.as_view(), name="logout"),
]
