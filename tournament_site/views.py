from django.shortcuts import render
from django.shortcuts import redirect


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

        return render(request, "tournament_site/tournament.html")

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
