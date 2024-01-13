from django.db import models


# Create your models here.
class Game(models.Model):
    alliance_number = models.IntegerField(default=0)


class Field(models.Model):
    field_number = models.IntegerField(unique=True)
    field_name = models.CharField(max_length=100)
    side1 = models.CharField(max_length=100)
    side2 = models.CharField(max_length=100)
    matches = models.ManyToManyField("Matches", blank=True)

    def __str__(self):
        return f"{self.field_name} ({self.field_number})"


class School(models.Model):
    school_name = models.CharField(max_length=100)
    number_of_teams = models.IntegerField(default=0)
    teams = models.ManyToManyField("Team")

    def __str__(self):
        return self.school_name


class Team(models.Model):
    number = models.IntegerField(unique=True)
    ranking_points = models.IntegerField(default=0)
    matches_played = models.IntegerField(default=0)
    alliance = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return str(self.number)


class Matches(models.Model):
    number = models.IntegerField(unique=True)
    time = models.TimeField(default="00:00:00")
    side1Team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name="side1Team")
    side2Team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name="side2Team")
    side1RankingPoints = models.IntegerField(default=0)
    side2RankingPoints = models.IntegerField(default=0)
    completed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.number}: {self.side1Team} vs {self.side2Team} @ {self.time}"


class Bracket(models.Model):
    Quarterfinals = models.ManyToManyField("PlayoffMatches", related_name="Quarterfinals", blank=True)
    Semifinals = models.ManyToManyField("PlayoffMatches", related_name="Semifinals", blank=True)
    Finals = models.ManyToManyField("PlayoffMatches", related_name="Finals", blank=True)
    Winner = models.ForeignKey(Team, on_delete=models.CASCADE, related_name="Winner", blank=True, null=True)


class PlayoffMatches(models.Model):
    id = models.IntegerField(unique=True, primary_key=True)
    side1Team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name="side1TeamPlayoff", blank=True, null=True)
    side2Team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name="side2TeamPlayoff", blank=True, null=True)
    winner = models.ForeignKey(Team, on_delete=models.CASCADE, related_name="winner", blank=True, null=True)

    def __str__(self):
        return f"{self.id}: {self.side1Team} vs {self.side2Team}"
