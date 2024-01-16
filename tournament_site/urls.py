from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("tournament/", views.tournament, name="tournament"),
    path("manage_tournament/", views.manage_tournament, name="manage_tournament"),
    path("login/", views.log_in, name="login"),
    path("logout/", views.log_out, name="logout"),
    path("alliance_selection/<int:alliance_number>/", views.alliance_selection, name="alliance_selection"),
    path("playoffs/", views.playoffs, name="playoffs"),
    path("views/", views.viewcompat, name="view site"),
                                
]
