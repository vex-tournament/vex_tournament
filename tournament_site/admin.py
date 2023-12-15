from django.contrib import admin
from .models import School, Team


@admin.register(School)
class SchoolAdmin(admin.ModelAdmin):
    pass


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    pass

# from django.contrib import admin
# from .models import Timer

# admin.site.register(Timer)