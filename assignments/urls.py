from django.urls import path, include
from .views import *


app_name = 'assignments'

urlpatterns = [
    path('add', CreateAssignmentView.as_view(), name="add-assign"),
    path('success', AssignSuccessView.as_view(), name="assign-success"),

    path('eval/<pk>', AssignDetailView.as_view(), name='assign-detail'),

    path('start-eval/<pk>', EvalAssignView.as_view(),
         name='assign-eval'),

    path('eval', AssignSelectView.as_view(), name="assign-select"),

]


