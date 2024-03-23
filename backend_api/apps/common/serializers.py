from rest_framework import serializers
from .models import Country, Location


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ["id", "name"]


class LocationSerializer(serializers.ModelSerializer):
    country = CountrySerializer()

    class Meta:
        model = Location
        fields = ["id", "name", "country"]

class CountryLocationsSerializer(serializers.ModelSerializer):
    locations = serializers.SerializerMethodField()
    class Meta:
        model = Country
        fields = ["id", "name", "locations"]

    def get_locations(self, obj):
        locations = Location.objects.filter(country_id=obj.id)
        return LocationSerializer(locations, many=True).data
