from django.db import models

from apps.core.models import BaseModel

"""
Common models shared across the apps
"""


class Country(BaseModel):
    name = models.CharField(max_length=200)

    class Meta:
        verbose_name = "Country"
        verbose_name_plural = "Countries"

    def __str__(self):
        return self.name

    # def get_country_code(self):
    #     country_code = pycountry.countries.get(name=self.name)
    #     if country_code is not None:
    #         return country_code.alpha_2
    #     return "N/A"


class Location(BaseModel):
    country = models.ForeignKey(
        Country,
        blank=False,
        null=True,
        on_delete=models.CASCADE,
        related_name="locations",
    )
    name = models.CharField(max_length=256)

    class Meta:
        verbose_name = "Location"
        verbose_name_plural = "Locations"


class Currency(BaseModel):
    name = models.CharField(max_length=200)
    initials = models.CharField(max_length=10)

    class Meta:
        verbose_name = "Currency"
        verbose_name_plural = "Currencies"


def country_choices():
    choices = {}
    try:
        for country in Country.objects.all():
            choices[country.name] = country.name
    except:
        pass

    return tuple(list(choices.items()))


def location_choices():
    choices = {}
    try:
        for location in Location.objects.all():
            choices[location.name] = location.name
    except:
        pass

    return tuple(list(choices.items()))
