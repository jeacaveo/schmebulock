""" Serializers of items app. """
from measurement.measures import Volume, Weight
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
    unit = serializers.CharField(max_length=32, required=True, write_only=True)

    class Meta:
        """ Meta data for serializer. """
        model = Item
        fields = ("id", "name", "price", "currency", "unit",
                  "volume", "weight", "brand", "order")

    def get_currency(self, obj):
        """
        Get currency from model instance.

        Currency it's generated from MoneyField and not actually in DB.

        """
        return obj.price_currency

    # Override
    def validate(self, attrs):
        """
        Custom validations for MoneyField.

        price field is marked as not required by default, in order to add the
        validation the field can't be overridden in Serializer or it breaks.

        """
        if not attrs.get("price"):
            raise serializers.ValidationError(
                {"price": "This field is required."})

        volume = attrs.get("volume")
        weight = attrs.get("weight")
        if not volume and not weight:
            raise serializers.ValidationError(
                {"volume": ["This field is required if "
                            "'weight' is not available."],
                 "weight": ["This field is required if "
                            "'volume' is not available."]})
        elif volume and weight:
            raise serializers.ValidationError(
                ["Either 'volume' or 'weight' must be provided, not both."])

        unit = attrs.get("unit")
        if volume and unit not in Volume.UNITS.keys():
            raise serializers.ValidationError(
                {"unit": ["'{}' is an invalid unit "
                          "for volume field.".format(unit)]})

        if weight and unit not in Weight.UNITS.keys():
            raise serializers.ValidationError(
                {"unit": ["'{}' is an invalid unit "
                          "for weight field.".format(unit)]})

        return attrs

    # Override
    def create(self, validated_data):
        """ Overriding to handle meassurement units. """
        validated_data.pop("unit")
        return super().create(validated_data)
