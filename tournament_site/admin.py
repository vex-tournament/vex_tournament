from django.contrib import admin
from .models import School, Team, GetTimer


@admin.register(School)
class SchoolAdmin(admin.ModelAdmin):
    pass


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    pass


@admin.register(GetTimer)
class GetTimeAdmin(admin.ModelAdmin):
    pass
