from django.contrib import admin
from .models import Field, School, Team, Matches, Bracket, PlayoffMatches


@admin.register(Field)
class FieldsAdmin(admin.ModelAdmin):
    pass


@admin.register(School)
class SchoolAdmin(admin.ModelAdmin):
    pass


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    pass


@admin.register(Matches)
class MatchesAdmin(admin.ModelAdmin):
    pass


@admin.register(Bracket)
class BracketAdmin(admin.ModelAdmin):
    pass


@admin.register(PlayoffMatches)
class PlayoffMatchesAdmin(admin.ModelAdmin):
    pass