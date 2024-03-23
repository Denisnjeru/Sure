from re import search
from django.contrib import admin
from django.template.loader import render_to_string
from .models import (
    Country, Location
)
@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    ordering = ('name', )
    search_fields = ('name', )

from apps.common.models import Country, Location

@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "country",
    ]
    list_filter = [
        "country"
    ]
    search_fields = [
        "name",
    ]