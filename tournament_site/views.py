from django.shortcuts import render
from django.shortcuts import redirect
from .models import School, Team


# Create your views here.
def index(request):
    if request.user.is_authenticated:
        return redirect("/tournament/")

    return render(request, "tournament_site/index.html")


# main tournament page, requires login
def tournament(request):
    if request.user.is_authenticated:
        # get user data
        user = request.user

        if user.is_staff:
            # staff user
            return redirect("/manage_tournament/")

        data = {
            "user": user,
            "schools": School.objects.all(),
            "teams": Team.objects.all()
        }

        # sort teams by ranking points
        data["teams"] = sorted(data["teams"], key=lambda team: team.ranking_points, reverse=True)

        return render(request, "tournament_site/tournament.html", data)

    return redirect("/login/")


# manage tournament page, requires login and staff status
def manage_tournament(request):
    if request.user.is_authenticated:
        # get user data
        user = request.user

        if user.is_staff:
            # staff user
            return render(request, "tournament_site/manage_tournament.html")

        return redirect("/tournament/")

    return redirect("/login/")
