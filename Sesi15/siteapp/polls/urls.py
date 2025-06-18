from django.urls import path

from . import views

urlpatterns = [
    path("raw", views.raw_index, name="index"),
    path("profile", views.profile, name="profile"),
    path("contact", views.contact, name="contact"),
    path("", views.html_index, name="html_index"),
    path("html", views.html_version, name="html_version"),
]