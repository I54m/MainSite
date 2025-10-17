from django.shortcuts import render
from django.views import generic
from portfolio.models import Project
from .models import PageContent, CarouselItem

def homepage(request):
	template_name = "basesite/homepage.html"
	context = {
		"carouselitems": CarouselItem.objects.filter(visible=True).order_by("position"),
		"pagecontent": PageContent.objects.get(page="HOME"),
		"featuredprojects": Project.objects.filter(featured=True, visible=True),
		}
	return render(request, template_name, context)

class AboutView(generic.ListView):
	template_name = 'basesite/about.html'
	context_object_name = 'pagecontent'

	def get_queryset(self): 
		"""Return content for the About page"""
		return PageContent.objects.get(page="ABOUT")

class ContactView(generic.ListView):
	template_name = 'basesite/contact.html'
	context_object_name = 'pagecontent'

	def get_queryset(self): 
		"""Return content for the Contact page"""
		return PageContent.objects.get(page="CONTACT")
