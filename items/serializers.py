""" Serializers of items app. """
from rest_framework import serializers

from .models import Brand, Order, Store, Item


class BrandSerializer(serializers.ModelSerializer):
    """ Serializer for Brand model. """

    class Meta:
        """ Meta data for serializer. """
        model = Brand
        fields = ("id", "name")


class StoreSerializer(serializers.ModelSerializer):
    """ Serializer for Store model. """

    class Meta:
        """ Meta data for serializer. """
        model = Store
        fields = ("id", "name")


class OrderSerializer(serializers.ModelSerializer):
    """ Serializer for Order model. """

    class Meta:
        """ Meta data for serializer. """
        model = Order
        fields = ("id", "date", "store")


class OrderNestedSerializer(serializers.ModelSerializer):
    """ Serializer for nested Order model. """

    store = StoreSerializer()

    class Meta:
        """ Meta data for serializer. """
        model = Order
        fields = ("id", "date", "store")


class ItemSerializer(serializers.ModelSerializer):
    """ Serializer for Item model. """
    currency = serializers.SerializerMethodField()

    class Meta:
        """ Meta data for serializer. """
        model = Item
        fields = ("id", "name", "price", "currency",
                  "volume", "weight", "brand", "order")

    def get_currency(self, obj):
        """
        Get currency from model instance.

        Currency it's generated from MoneyField and not actually in DB.

        """
        return obj.price_currency

    def validate(self, attrs):
        """
        Custom validations for MoneyField.

        price field is marked as not required by default, in order to add the
        validation the field can't be overridden in Serializer or it breaks.

        """
        if not attrs.get("price"):
            raise serializers.ValidationError(
                {"price": "This field is required."})
        return attrs
