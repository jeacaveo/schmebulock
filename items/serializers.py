""" Serializers of items app. """
from rest_framework import serializers

from .models import Brand, Order, Store


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


class OrderSerializer(serializers.ModelSerializer):
    """ Serializer for Order model. """

    class Meta:
        """ Meta data for serializer. """
        model = Order
        fields = ('id', 'date', 'store')


class OrderNestedSerializer(serializers.ModelSerializer):
    """ Serializer for nested Order model. """

    store = StoreSerializer()

    class Meta:
        """ Meta data for serializer. """
        model = Order
        fields = ('id', 'date', 'store')
