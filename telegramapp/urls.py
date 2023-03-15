from django.urls import path

from . import views

urlpatterns = [
    path("teleg/", views.teleg, name="teleg")
]
