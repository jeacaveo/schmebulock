""" Serializers of items app. """
from rest_framework import serializers

from .models import Brand, Store


class BrandSerializer(serializers.ModelSerializer):
    """ Serializer for Brand model. """

    class Meta:
        """ Meta data for serializer. """
        model = Brand
        fields = ('id', 'name')


class StoreSerializer(serializers.ModelSerializer):
    """ Serializer for Store model. """

    class Meta:
        """ Meta data for serializer. """
        model = Store
        fields = ('id', 'name')
