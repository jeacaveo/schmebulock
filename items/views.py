""" Views of items app. """

from rest_framework import viewsets

from . import models
from . import serializers


class BrandViewSet(viewsets.ModelViewSet):
    """ Endpoint for Brands. """
    queryset = models.Brand.objects.all()
    serializer_class = serializers.BrandSerializer
    # permission_classes = [IsAccountAdminOrReadOnly]
