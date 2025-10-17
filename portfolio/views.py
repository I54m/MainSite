from django.shortcuts import render, get_object_or_404
from django.views import generic
from django.utils import timezone
from .models import Project, Category

class ProjectListView(generic.ListView):
	template_name = 'portfolio/projects.html'
	context_object_name = 'categorys'

	def get_queryset(self): 
		"""Return the all visible categories ordered by their position."""
		return Category.objects.filter(visible=True).order_by('position')


class DetailView(generic.DetailView):
	model = Project
	template_name = 'portfolio/detail.html'
	def get_queryset(self): 
		"""
		Return all projects
		"""
		return Project.objects.all()