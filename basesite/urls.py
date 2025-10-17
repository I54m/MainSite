from django.urls import path

from . import views

app_name = "basesite"

urlpatterns = [
    path("", views.homepage, name="homepage"),
    # ex /about/
    path("about/", views.AboutView.as_view(), name="about"),
    # ex /contact/
    path("contact/", views.ContactView.as_view(), name="contact"),
]
 