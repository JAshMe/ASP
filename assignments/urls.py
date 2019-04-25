from django.urls import path, include
from .views import *


app_name = 'assignments'

urlpatterns = [
    path('add_assign', CreateAssignmentView.as_view(), name="add-assign"),
    path('assign_success', AssignSuccessView.as_view(), name="assign-success")
]
