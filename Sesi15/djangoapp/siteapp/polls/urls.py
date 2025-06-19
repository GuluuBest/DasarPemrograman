from django.urls import path
from . import views

app_name = 'polls'

urlpatterns = [
    path("", views.html_index, name="index"),
    path('<int:question_id>/', views.detail, name='detail'),
    path('<int:question_id>/vote/', views.vote, name='vote'),
    path('<int:question_id>/results/', views.results, name='results'),
    path("profile/", views.profile, name="profile"),
    path("contact/", views.contact, name="contact"),
    path("address/", views.address, name="address"),
    path("phone/", views.phone, name="phone"),
]