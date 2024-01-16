from django.shortcuts import render
from django.shortcuts import redirect
from .models import Field, School, Team, Matches, PlayoffMatches, Bracket
from django.contrib.auth import authenticate, login, logout
from django import forms


def goodRound(num):
    # 0.5 is the threshold for rounding up
    if num % 1 >= 0.5:
        return int(num) + 1
    else:
        return int(num)


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


class playoffMatchForm(forms.Form):
    match_type = forms.CharField(label="Match Type")
    match_id = forms.IntegerField(label="Match ID")
    number = forms.IntegerField(label="Match Number")
    winner = forms.IntegerField(label="Winner")

    def clean(self):
        cleaned_data = super(playoffMatchForm, self).clean()
        match_type = cleaned_data.get("match_type")
        number = cleaned_data.get("number")
        winner = cleaned_data.get("winner")

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
            if Bracket.objects.all().count() != 0:
                # redirect to playoffs if bracket has been created, meaning playoffs have started
                return redirect("/playoffs/")

            if request.method == "POST":
                # handle form
                form = MatchForm(request.POST)

                if form.is_valid():
                    # get match
                    match = Matches.objects.get(number=form.cleaned_data["match_number"])

                    # update team ranking points
                    side1RPDiff = form.cleaned_data["side1Points"] - match.side1RankingPoints
                    side2RPDiff = form.cleaned_data["side2Points"] - match.side2RankingPoints

                    # get team
                    team11 = Team.objects.get(number=match.side1Team1.number)
                    team12 = Team.objects.get(number=match.side1Team2.number)
                    team21 = Team.objects.get(number=match.side2Team1.number)
                    team22 = Team.objects.get(number=match.side2Team2.number)

                    # update ranking points
                    team11.ranking_points += side1RPDiff
                    team12.ranking_points += side1RPDiff
                    team21.ranking_points += side2RPDiff
                    team22.ranking_points += side2RPDiff

                    # update matches played
                    if form.cleaned_data["completed"] and not match.completed:
                        team11.matches_played += 1
                        team12.matches_played += 1
                        team21.matches_played += 1
                        team22.matches_played += 1
                    elif not form.cleaned_data["completed"] and match.completed:
                        team11.matches_played -= 1
                        team12.matches_played -= 1
                        team21.matches_played -= 1
                        team22.matches_played -= 1

                    # save teams
                    team11.save()
                    team12.save()
                    team21.save()
                    team22.save()                        

                    # update match
                    match.side1RankingPoints = form.cleaned_data["side1Points"]
                    match.side2RankingPoints = form.cleaned_data["side2Points"]
                    match.completed = form.cleaned_data["completed"]
                    match.save()

            # fields
            fields = Field.objects.all()
            matches = Matches.objects.all().order_by("number")
            teams = reversed(Team.objects.all().order_by("ranking_points"))

            return render(
                request,
                "tournament_site/manage_tournament.html",
                {"fields": fields, "matches": matches, "teams": teams}
            )

        return redirect("/tournament/")

    return redirect("/login/")

def view(request):
    fields = Field.objects.all()
    matches = Matches.objects.all().order_by("number")
    teams = reversed(Team.objects.all().order_by("ranking_points"))

    return render(
        request,
        "tournament_site/manage_tournament.html",
        {"fields": fields, "matches": matches, "teams": teams}
    )

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


def alliance_selection(request, alliance_number):
    # get teams, sorted by ranking points
    user = request.user

    if not user.is_staff:
        return redirect("/tournament/")

    if Bracket.objects.all().count() != 0:
        # redirect to playoffs if bracket has been created, meaning playoffs have started
        return redirect("/playoffs/")

    if request.method == "POST":
        teams = Team.objects.all()
        playoff_teams = [None]*8

        number_of_teams = 0

        for team in teams:
            position = request.POST.get(f"{team.number}_position")

            if position != "None":
                playoff_teams[int(position) - 1] = team
                number_of_teams += 1

        for team in teams:
            alliance = request.POST.get(str(team.number))

            if alliance == "None":
                team.alliance = None
                team.save()
                continue

            team.alliance = Team.objects.get(number=int(alliance))
            team.save()

        # put teams into brackets, filtering out None teams
        teams = Team.objects.all()



        seenTeams = set()  # avoid duplicate teams

        matches = []

        # it is guaranteed that there will be an even number of teams with an alliance, so we can safely divide by two
        if number_of_teams // 2 % 2 == 1:
            # add a bye for the first team if there is an odd number of teams
            bye_match = PlayoffMatches.objects.create(
                id=PlayoffMatches.objects.all().count(),
                side1Team=playoff_teams[0],
                side2Team=None
            )

            seenTeams.add(playoff_teams[0].number)
            seenTeams.add(playoff_teams[0].alliance.number)

            empty_match = PlayoffMatches.objects.create(id=PlayoffMatches.objects.all().count(), winner=playoff_teams[0])
        else:
            bye_match = None

        # we can utilize rounding here because the answer will either be even or odd, and we want to increase the
        # number by one if it is odd
        match_num = goodRound(number_of_teams / 4)
        alliance_num = number_of_teams // 2

        for pos in range(match_num):
            team = playoff_teams[pos]

            # team2 is the i - pos team
            if bye_match is None:
                side2Team = playoff_teams[alliance_num - pos - 1]
            else:
                side2Team = playoff_teams[alliance_num - pos]

            if team.number in seenTeams:
                continue

            seenTeams.add(team.number)
            seenTeams.add(team.alliance.number)
            playoff_match = PlayoffMatches.objects.create(
                id=PlayoffMatches.objects.all().count(),
                side1Team=team,
                side2Team=side2Team
            )

            matches.append(playoff_match)

        bracket = Bracket.objects.create()

        if match_num > 2:
            print(bye_match)
            if bye_match is not None:
                bye_match.id = 5
                bye_match.save()
                bracket.Quarterfinals.add(empty_match)
                bracket.Semifinals.add(bye_match)
            else:
                bracket.Semifinals.add(PlayoffMatches.objects.create(id=5))

            for match in matches:
                bracket.Quarterfinals.add(match)

            # add the other SemiFinals match
            bracket.Semifinals.add(PlayoffMatches.objects.create(id=6))

            # add 1 empty final match
            bracket.Finals.add(PlayoffMatches.objects.create(id=7))
        elif match_num > 1:
            if bye_match is not None:
                bye_match.id = 7
                bye_match.save()
                bracket.Finals.add(bye_match)
                bracket.Semifinals.add(empty_match)
            else:
                # add 1 empty final match
                bracket.Finals.add(PlayoffMatches.objects.create(id=7))

            for match in matches:
                bracket.Semifinals.add(match)
        else:
            bracket.Finals.add(matches[0])

        return redirect("/playoffs/")

    teams = Team.objects.all()
    teams = sorted(teams, key=lambda team: team.ranking_points, reverse=True)

    return render(request, "tournament_site/alliance_selection.html",
                  {"teams": teams, "alliance_number": alliance_number, "range8": range(1, 9)})


def playoffs(request):
    user = request.user

    if not user.is_staff:
        return redirect("/tournament/")

    if request.method == "POST":
        form = playoffMatchForm(request.POST)

        if form.is_valid():
            match_type = form.cleaned_data["match_type"]
            match_id = form.cleaned_data["match_id"]
            number = form.cleaned_data["number"]
            winner = form.cleaned_data["winner"]

            if match_type == "quarterFinals":
                match = Bracket.objects.all()[0].Quarterfinals.get(id=match_id)
            elif match_type == "semiFinals":
                match = Bracket.objects.all()[0].Semifinals.get(id=match_id)
            else:
                match = Bracket.objects.all()[0].Finals.get(id=match_id)

            match.winner = Team.objects.get(number=winner)
            match.save()

            if match_type == "quarterFinals":
                if number < 2:
                    # get next match
                    nextMatch = Bracket.objects.all()[0].Semifinals.get(id=5)
                else:
                    nextMatch = Bracket.objects.all()[0].Semifinals.get(id=6)

                if number % 2 == 0:
                    nextMatch.side1Team = match.winner
                else:
                    nextMatch.side2Team = match.winner
            elif match_type == "semiFinals":
                nextMatch = Bracket.objects.all()[0].Finals.get(id=7)

                if number % 2 == 0:
                    nextMatch.side1Team = match.winner
                else:
                    nextMatch.side2Team = match.winner
            else:
                nextMatch = Bracket.objects.all()[0]
                nextMatch.Winner = match.winner

            nextMatch.save()

        return redirect("/playoffs/")

    teams = Team.objects.filter(alliance__isnull=False)
    teams = sorted(teams, key=lambda team: team.ranking_points, reverse=True)

    quarterFinals = list(Bracket.objects.all()[0].Quarterfinals.all())
    semiFinals = Bracket.objects.all()[0].Semifinals.all()
    finals = Bracket.objects.all()[0].Finals.all()
    winner = Bracket.objects.all()[0].Winner

    quarterFinalsEnabled = [False]*4
    semiFinalsEnabled = [False]*2
    finalsEnabled = False

    # swap the second and third matches
    if len(quarterFinals) > 1:
        temp = quarterFinals[1]
        quarterFinals[1] = quarterFinals[2]
        quarterFinals[2] = temp

    for pos, match in enumerate(quarterFinals):
        if match.side1Team is not None or match.side2Team is not None:
            quarterFinalsEnabled[pos] = True

    for pos, match in enumerate(semiFinals):
        if match.side1Team is not None or match.side2Team is not None:
            semiFinalsEnabled[pos] = True

    if finals[0].side1Team is not None or finals[0].side2Team is not None:
        finalsEnabled = True

    return render(request, "tournament_site/playoffs.html",
                  {"teams": teams, "quarterFinals": quarterFinals, "semiFinals": semiFinals, "finals": finals, "winner": winner,
                   "quarterFinalsEnabled": quarterFinalsEnabled, "semiFinalsEnabled": semiFinalsEnabled, "finalsEnabled": finalsEnabled})
