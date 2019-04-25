from django.shortcuts import render
from django.views.generic import TemplateView, CreateView


class IndexView(TemplateView):
    template_name = 'assignments/index.html'

class CreateAssignmentView()

