from itertools import count
from django.shortcuts import render

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import pagination

from apps.common.models import Country, Location
from apps.common.serializers import CountrySerializer, LocationSerializer, CountryLocationsSerializer
from apps.core.models import CategoryType
from apps.core.serializers import CategoryTypeSerializer


class CountryView(viewsets.ModelViewSet):
    http_method_names = ["get"]

    def get_serializer_class(self):
        return CountrySerializer

    def get_queryset(self):
        return Country.objects.all()

    @action(methods=["get"],detail=False,url_path="country/locations/(?P<country_id>\d+)",)
    def get_locations(self,request,country_id):
        country = Country.objects.filter(id=country_id).first()
        print(request)
        print(country)

        if country is not None:
            locations = Location.objects.filter(country=country).order_by("id")
            res = CountrySerializer(locations, many=True)
            context = {"locations": res.data}
            return Response(context, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)

    @action(methods=['get'], detail=False, url_path='(?P<country_name>[\w\-]+)/locations')
    def country_locations(self, request, country_name):
        print(country_name)

        country = Country.objects.filter(name=country_name).first()
        serializer = CountryLocationsSerializer(country)
        return Response(serializer.data, status=status.HTTP_200_OK)


class LocationView(viewsets.ModelViewSet):
    http_method_names = ["get"]
    pagination.PageNumberPagination.page_size = 400 

    def get_serializer_class(self):
        return LocationSerializer

    def get_queryset(self):
        return Location.objects.all()

class CategoryTypeView(viewsets.ModelViewSet):
    http_method_names = ["get"]
    pagination.PageNumberPagination.page_size = 400 

    def get_serializer_class(self):
        return CategoryTypeSerializer

    def get_queryset(self):
        return CategoryType.objects.all()
