from django.contrib import admin
from .models import Field, School, Team, Matches


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
