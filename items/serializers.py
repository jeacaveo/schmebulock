""" Serializers of items app. """
from rest_framework import serializers

from .models import Brand


class BrandSerializer(serializers.ModelSerializer):
    """ Serializer for Brand model. """

    class Meta:  # pylint: disable=too-few-public-methods
        """ Meta data for serializer. """
        model = Brand
        fields = ('id', 'name')
