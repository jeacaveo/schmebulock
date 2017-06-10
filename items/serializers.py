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
    currency = serializers.CharField(source="price_currency", required=False)
    unit = serializers.CharField(max_length=32, required=True, write_only=True)

    class Meta:
        """ Meta data for serializer. """
        model = Item
        fields = ("id", "name", "price", "currency", "unit",
                  "volume", "weight", "brand", "order")

    # Override
    def validate(self, attrs):
        """
        Custom validations for MoneyField and MeasurementField.

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
    def to_representation(self, instance):
        """
        Overriding to handle MeasurementFields independently since the
        value is exposed in different way (an object instead of the number).

        unit is a custom field that needs to get data from volume or weight.

        """
        measurement_fields = [
            item for item in self._readable_fields
            if item.field_name in ["volume", "weight"]]

        self._readable_fields = [
            item for item in self._readable_fields
            if item.field_name not in ["volume", "weight"]]
        ret = super().to_representation(instance)

        for field in measurement_fields:
            attr = field.get_attribute(instance)
            ret[field.field_name] = float(attr.value) if attr else None

        # Volume or Weight must always be present, but in case they are
        # both empty, doing last line of validations.
        ret["unit"] = (instance.volume.unit
                       if instance.volume
                       else instance.weight.unit if instance.weight else None)

        return ret

    # Override
    def create(self, validated_data):
        """ Overriding to handle meassurement units. """
        unit = validated_data.pop("unit", None)
        volume = validated_data.get("volume")
        weight = validated_data.get("weight")
        if volume:
            validated_data["volume"] = Volume(
                **{unit or "cubic_meter": volume})
        elif weight:
            validated_data["weight"] = Weight(
                **{unit or "g": weight})

        return super().create(validated_data)

    # Override
    def update(self, instance, validated_data):
        """ Overriding to handle meassurement units. """
        unit = validated_data.get("unit", None)
        volume = (validated_data.get("volume") or
                  instance.volume.value if instance.volume else None)
        weight = (validated_data.get("weight") or
                  instance.weight.value if instance.weight else None)
        if volume:
            validated_data["volume"] = Volume(
                **{unit or "cubic_meter": volume})
        elif weight:
            validated_data["weight"] = Weight(
                **{unit or "g": weight})

        return super().update(instance, validated_data)


class ItemNestedSerializer(serializers.ModelSerializer):
    """ Serializer for nested Item model. """

    currency = serializers.CharField(source="price_currency", required=False)
    unit = serializers.SerializerMethodField()
    volume = serializers.FloatField(source="volume.value")
    weight = serializers.FloatField(source="weight.value")
    brand = StoreSerializer()
    order = OrderNestedSerializer()

    class Meta:
        """ Meta data for serializer. """
        model = Item
        fields = ("id", "name", "price", "currency", "unit",
                  "volume", "weight", "brand", "order")

    def get_unit(self, obj):
        """ Custom field that needs to get data from volume or weight. """
        # Volume or Weight must always be present, but in case they are
        # both empty, doing last line of validations.
        return (obj.volume.unit if obj.volume
                else obj.weight.unit if obj.weight else None)
