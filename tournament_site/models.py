from django.db import models


# Create your models here.
class School(models.Model):
    school_name = models.CharField(max_length=100)
    number_of_teams = models.IntegerField()
    teams = models.ManyToManyField("Team")


class Team(models.Model):
    team_name = models.CharField(max_length=100)
    team_number = models.IntegerField()
    ranking_points = models.IntegerField(default=0)
    matches_played = models.IntegerField(default=0)
