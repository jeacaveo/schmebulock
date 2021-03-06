""" Views of items app. """

from rest_framework import viewsets

from . import models
from . import serializers
from . import metadata


class BrandViewSet(viewsets.ModelViewSet):
    """ Endpoint for Brands. """
    queryset = models.Brand.objects.all()
    serializer_class = serializers.BrandSerializer


class StoreViewSet(viewsets.ModelViewSet):
    """ Endpoint for Stores. """
    queryset = models.Store.objects.all()
    serializer_class = serializers.StoreSerializer


class OrderViewSet(viewsets.ModelViewSet):
    """
    Endpoint for Orders.

    GET parameters:

        'nested' (boolean): get detailed information on foreign key fields.

    """
    queryset = models.Order.objects.all()
    serializer_class = serializers.OrderSerializer

    # Override
    def get_serializer_class(self):
        """
        Override!

        Using custom nested serializer when requested.

        """
        if (self.request.method == "GET" and
                self.request.query_params.get("nested")):
            return serializers.OrderNestedSerializer
        return super().get_serializer_class()


class ItemViewSet(viewsets.ModelViewSet):
    """
    Endpoint for Items.

    GET parameters:

        'nested' (boolean): get detailed information on foreign key fields.

    """
    queryset = models.Item.objects.all()
    serializer_class = serializers.ItemSerializer
    metadata_class = metadata.CustomItemMetadata

    # Override
    def get_serializer_class(self):
        """
        Override!

        Using custom nested serializer when requested.

        """
        if (self.request.method == "GET" and
                self.request.query_params.get("nested")):
            return serializers.ItemNestedSerializer
        return super().get_serializer_class()


class LocationViewSet(viewsets.ModelViewSet):
    """
    Endpoint for Location.

    GET parameters:

        'nested' (boolean): get detailed information on foreign key fields.

    """
    queryset = models.Location.objects.all()
    serializer_class = serializers.LocationSerializer

    # Override
    def get_serializer_class(self):
        """
        Override!

        Using custom nested serializer when requested.

        """
        if (self.request.method == "GET" and
                self.request.query_params.get("nested")):
            return serializers.LocationNestedSerializer
        return super().get_serializer_class()


class PurchaseViewSet(viewsets.ModelViewSet):
    """
    Endpoint for Purchase.

    GET parameters:

        'nested' (boolean): get detailed information on foreign key fields.

    """
    queryset = models.Purchase.objects.all()
    serializer_class = serializers.PurchaseSerializer
    metadata_class = metadata.CustomPurchaseMetadata

    # Override
    def get_serializer_class(self):
        """
        Override!

        Using custom nested serializer when requested.

        """
        if (self.request.method == "GET" and
                self.request.query_params.get("nested")):
            return serializers.PurchaseNestedSerializer
        return super().get_serializer_class()
