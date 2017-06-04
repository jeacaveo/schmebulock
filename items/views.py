""" Views of items app. """

from rest_framework import viewsets

from . import models
from . import serializers


class BrandViewSet(viewsets.ModelViewSet):
    """ Endpoint for Brands. """
    queryset = models.Brand.objects.all()
    serializer_class = serializers.BrandSerializer


class StoreViewSet(viewsets.ModelViewSet):
    """ Endpoint for Stores. """
    queryset = models.Store.objects.all()
    serializer_class = serializers.StoreSerializer


class OrderViewSet(viewsets.ModelViewSet):
    """ Endpoint for Order. """
    queryset = models.Order.objects.all()
    serializer_class = serializers.OrderSerializer
