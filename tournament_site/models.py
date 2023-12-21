from django.db import models


# Create your models here.
class Field(models.Model):
    field_number = models.IntegerField(unique=True)
    field_name = models.CharField(max_length=100)
    side1 = models.CharField(max_length=100)
    side2 = models.CharField(max_length=100)
    matches = models.ManyToManyField("Matches", blank=True)


class School(models.Model):
    school_name = models.CharField(max_length=100)
    number_of_teams = models.IntegerField(default=0)
    teams = models.ManyToManyField("Team")


class Team(models.Model):
    number = models.IntegerField(unique=True)
    ranking_points = models.IntegerField(default=0)
    matches_played = models.IntegerField(default=0)


class Matches(models.Model):
    number = models.IntegerField(unique=True)
    time = models.TimeField(default="00:00:00")
    side1Team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name="side1Team")
    side2Team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name="side2Team")
    side1RankingPoints = models.IntegerField(default=0)
    side2RankingPoints = models.IntegerField(default=0)
    completed = models.BooleanField(default=False)
