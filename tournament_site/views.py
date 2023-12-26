from django.shortcuts import render
from django.shortcuts import redirect
from .models import Field, School, Team, Matches
from django.contrib.auth import authenticate, login, logout
from django import forms


class LoginForm(forms.Form):
    username = forms.CharField(label="Username", max_length=100)
    password = forms.CharField(label="Password", max_length=100, widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super(LoginForm, self).clean()
        username = cleaned_data.get("username")
        password = cleaned_data.get("password")

        if not authenticate(username=username, password=password):
            raise forms.ValidationError("Invalid username or password")

        return cleaned_data


class MatchForm(forms.Form):
    match_number = forms.IntegerField(label="Match Number")
    side1Points = forms.IntegerField(label="Side 1 Points")
    side2Points = forms.IntegerField(label="Side 2 Points")
    completed = forms.BooleanField(label="Completed", required=False)

    def clean(self):
        cleaned_data = super(MatchForm, self).clean()
        match_number = cleaned_data.get("match_number")
        side1Points = cleaned_data.get("side1Points")
        side2Points = cleaned_data.get("side2Points")
        completed = cleaned_data.get("completed")

        if not Matches.objects.filter(number=match_number).exists():
            raise forms.ValidationError("Invalid match number")

        if side1Points < 0 or side2Points < 0:
            raise forms.ValidationError("Invalid points")

        return cleaned_data


# Create your views here.
def index(request):
    if request.user.is_authenticated:
        return redirect("/tournament/")

    return redirect("/login/")


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
            if request.method == "POST":
                # handle form
                form = MatchForm(request.POST)

                if form.is_valid():
                    # get match
                    match = Matches.objects.get(number=form.cleaned_data["match_number"])

                    # update match
                    match.side1RankingPoints = form.cleaned_data["side1Points"]
                    match.side2RankingPoints = form.cleaned_data["side2Points"]
                    match.completed = form.cleaned_data["completed"]
                    match.save()

            # fields
            fields = Field.objects.all()
            matches = Matches.objects.all().order_by("time")
            teams = Team.objects.all().order_by("ranking_points")

            return render(
                request,
                "tournament_site/manage_tournament.html",
                {"fields": fields, "matches": matches, "teams": teams}
            )

        return redirect("/tournament/")

    return redirect("/login/")


def log_in(request):
    if request.user.is_authenticated:
        return redirect("/tournament/")

    if request.method == "POST":
        form = LoginForm(request.POST)

        if form.is_valid():
            user = authenticate(username=form.cleaned_data["username"], password=form.cleaned_data["password"])
            login(request, user)
            return redirect("/tournament/")
    else:
        form = LoginForm()

    return render(request, "tournament_site/login.html", {"form": form})


def log_out(request):
    logout(request)
    return redirect("/login/")
