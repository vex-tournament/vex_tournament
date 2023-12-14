from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("tournament/", views.tournament, name="tournament"),
    path("manage_tournament/", views.manage_tournament, name="manage_tournament")
]
