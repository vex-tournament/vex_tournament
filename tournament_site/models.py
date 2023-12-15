from django.db import models


# Create your models here.
class School(models.Model):
    school_name = models.CharField(max_length=100)
    number_of_teams = models.IntegerField(default=0)
    teams = models.ManyToManyField("Team")


class Team(models.Model):
    team_number = models.IntegerField(unique=True)
    ranking_points = models.IntegerField(default=0)
    matches_played = models.IntegerField(default=0)


class GetTimer(models.Model):
    timer = models.IntegerField(default=0)