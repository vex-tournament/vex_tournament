from django.contrib import admin
from .models import School, Team


@admin.register(School)
class SchoolAdmin(admin.ModelAdmin):
    pass


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    pass
