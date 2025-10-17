from django.urls import path

from . import views

app_name = "portfolio"

urlpatterns = [
    # ex: /projects/
    path("projects/", views.ProjectListView.as_view(), name="projects"),
    # ex: /projects/project-slug/
    path("projects/<slug:slug>/", views.DetailView.as_view(), name="detail"),
]
 