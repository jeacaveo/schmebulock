""" Test for all serializers of items app. """
from json import dumps, loads

from django.test import TestCase
from measurement.measures import Volume, Weight

from model_mommy import mommy

from ..serializers import (
    BrandSerializer,
    ItemSerializer,
    ItemNestedSerializer,
    OrderSerializer,
    OrderNestedSerializer,
    PurchaseSerializer,
    PurchaseNestedSerializer,
    StoreSerializer)


class BrandSerializerTest(TestCase):
    """ Tests for Brand serializer. """

    def test_fields(self):
        """ Test fields for serializer. """
        # Given
        expected_data = {"name": ""}

        # When
        serializer = BrandSerializer()

        # Then
        self.assertEqual(serializer.data, expected_data)


class StoreSerializerTest(TestCase):
    """ Tests for Store serializer. """

    def test_fields(self):
        """ Test fields for serializer. """
        # Given
        expected_data = {"name": ""}

        # When
        serializer = StoreSerializer()

        # Then
        self.assertEqual(serializer.data, expected_data)


class OrderSerializerTest(TestCase):
    """ Tests for Order serializer. """

    def test_fields(self):
        """ Test fields for serializer. """
        # Given
        expected_data = {"date": None, "store": None}

        # When
        serializer = OrderSerializer()

        # Then
        self.assertEqual(serializer.data, expected_data)


class OrderNestedSerializerTest(TestCase):
    """ Tests for nested Order serializer. """

    def test_fields(self):
        """ Test fields for serializer. """
        # Given
        store = mommy.make("Store")
        expected_data = {"date": None,
                         "store": {"id": store.id, "name": store.name}}

        # When
        serializer = OrderNestedSerializer({"date": None, "store": store})

        # Then
        self.assertEqual(serializer.data, expected_data)


class ItemSerializerTest(TestCase):
    """ Tests for Item serializer. """
    def setUp(self):
        self.default_volume_unit = "cubic_meter"
        self.default_weight_unit = "g"
        self.brand = mommy.make("Brand")

    def test_fields_data(self):
        """ Test fields for serializer. """
        # Given
        item = mommy.make("Item",
                          volume=Volume(l=1),  # noqa
                          weight=Weight(g=1))
        item.refresh_from_db()  # To trigger MeasurementField updates
        expected_data = {
            "id": item.id, "name": item.name, "brand": item.brand.id,
            "unit": self.default_volume_unit, "volume": 0.001, "weight": 1}

        # When
        serializer = ItemSerializer(item)

        # Then
        self.assertEqual(serializer.data, expected_data)

    def test_errors_empty(self):
        """ Test errors on empty data. """
        # Given
        expected_data = {"name": ["This field is required."],
                         "unit": ["This field is required."],
                         "brand": ["This field is required."]}
        data = {}

        # When
        serializer = ItemSerializer(data=data)
        serializer.is_valid()

        # Then
        self.assertEqual(serializer.errors, expected_data)

    def test_errors_null(self):
        """ Test errors when required fields are null. """
        # Given
        expected_data = {"name": ["This field may not be null."],
                         "unit": ["This field may not be null."],
                         "brand": ["This field may not be null."]}
        data = {"name": None, "unit": None, "brand": None}

        # When
        serializer = ItemSerializer(data=data)
        serializer.is_valid()

        # Then
        self.assertEqual(serializer.errors, expected_data)

    def test_errors_no_volume_weight(self):
        """
        Test errors when both volume and weight fields are not provided.

        """
        # Given
        expected_data = {"volume": ["This field is required if "
                                    "'weight' is not available."],
                         "weight": ["This field is required if "
                                    "'volume' is not available."]}
        data = {"name": "Item X", "brand": self.brand.id,
                "unit": self.default_weight_unit}

        # When
        serializer = ItemSerializer(data=data)
        serializer.is_valid()

        # Then
        self.assertEqual(serializer.errors, expected_data)

    def test_errors_both_volume_weight(self):
        """ Test errors when both volume and weight fields are provided. """
        # Given
        expected_data = {
            "non_field_errors": ["Either 'volume' or 'weight' must be "
                                 "provided, not both."]}
        data = {"name": "Item X", "brand": self.brand.id,
                "unit": self.default_weight_unit, "volume": 100, "weight": 100}

        # When
        serializer = ItemSerializer(data=data)
        serializer.is_valid()

        # Then
        self.assertEqual(serializer.errors, expected_data)

    def test_errors_invalid_volume_unit(self):
        """ Test errors when volume is provided with an invalid unit. """
        # Given
        expected_data = {
            "unit": ["'invalid_unit' is an invalid unit for volume field."]}
        data = {"name": "Item X", "brand": self.brand.id,
                "unit": "invalid_unit", "volume": 100}

        # When
        serializer = ItemSerializer(data=data)
        serializer.is_valid()

        # Then
        self.assertEqual(serializer.errors, expected_data)

    def test_errors_invalid_weight_unit(self):
        """ Test errors when weight is provided with an invalid unit. """
        # Given
        expected_data = {
            "unit": ["'invalid_unit' is an invalid unit for weight field."]}
        data = {"name": "Item X", "brand": self.brand.id,
                "unit": "invalid_unit", "weight": 100}

        # When
        serializer = ItemSerializer(data=data)
        serializer.is_valid()

        # Then
        self.assertEqual(serializer.errors, expected_data)

    def test_save_volume_default_unit(self):
        """ Test successful save when volume is provided with default unit. """
        # Given
        data = {"name": "Item X", "brand": self.brand.id,
                "unit": self.default_volume_unit, "volume": 100}

        # When
        serializer = ItemSerializer(data=data)
        serializer.is_valid()
        obj = serializer.save()

        # Then
        obj.refresh_from_db()
        self.assertEqual(obj.volume.unit, self.default_volume_unit)
        self.assertEqual(obj.volume.value, 100.0)
        self.assertEqual(obj.volume.standard, 100.0)
        self.assertEqual(obj.volume.cubic_meter, 100.0)
        self.assertEqual(obj.brand, self.brand)

    def test_save_volume_another_unit(self):
        """
        Test successful save when volume is provided with a unit
        different than the default one.

        """
        # Given
        expected_value = 0.1
        data = {"name": "Item X", "brand": self.brand.id,
                "unit": "l", "volume": 100}

        # When
        serializer = ItemSerializer(data=data)
        serializer.is_valid()
        obj = serializer.save()

        # Then
        obj.refresh_from_db()
        self.assertEqual(obj.volume.l, 100.0)
        self.assertEqual(obj.volume.unit, self.default_volume_unit)
        self.assertEqual(obj.volume.value, expected_value)
        self.assertEqual(obj.volume.standard, expected_value)
        self.assertEqual(obj.volume.cubic_meter, expected_value)
        self.assertEqual(obj.brand, self.brand)

    def test_save_weight_default_unit(self):
        """ Test successful save when weight is provided. """
        # Given
        data = {"name": "Item X", "brand": self.brand.id,
                "unit": self.default_weight_unit, "weight": 100}

        # When
        serializer = ItemSerializer(data=data)
        serializer.is_valid()
        obj = serializer.save()

        # Then
        obj.refresh_from_db()
        self.assertEqual(obj.weight.unit, self.default_weight_unit)
        self.assertEqual(obj.weight.value, 100.0)
        self.assertEqual(obj.weight.standard, 100.0)
        self.assertEqual(obj.weight.g, 100.0)
        self.assertEqual(obj.brand, self.brand)

    def test_save_weight_another_unit(self):
        """
        Test successful save when weight is provided with a unit
        different than the default one.

        """
        # Given
        expected_value = 2834.95
        data = {"name": "Item X", "brand": self.brand.id,
                "unit": "oz", "weight": 100}

        # When
        serializer = ItemSerializer(data=data)
        serializer.is_valid()
        obj = serializer.save()

        # Then
        obj.refresh_from_db()
        self.assertEqual(obj.weight.oz, 100)
        self.assertEqual(obj.weight.unit, self.default_weight_unit)
        self.assertEqual(obj.weight.value, expected_value)
        self.assertEqual(obj.weight.standard, expected_value)
        self.assertEqual(obj.weight.g, expected_value)
        self.assertEqual(obj.brand, self.brand)

    def test_update_standard_field(self):
        """
        Test successful update when updating a fields that's not
        volume or weight.

        """
        # Given
        expected_name = "Item X"
        item = mommy.make("Item", name="XXXXXX", volume=Volume(cubic_meter=10))

        # When
        serializer = ItemSerializer(item)
        serializer.update(item, {"name": expected_name})

        # Then
        item.refresh_from_db()
        self.assertEqual(item.name, expected_name)

    def test_update_volume(self):
        """ Test successful update of volume. """
        # Given
        expected_value = 100
        expected_standard_value = 0.1
        item = mommy.make("Item", volume=Volume(cubic_meter=99))

        # When
        serializer = ItemSerializer(item)
        serializer.update(item,
                          {"unit": "l", "volume": expected_value})

        # Then
        item.refresh_from_db()
        self.assertEqual(item.volume.l, expected_value)
        self.assertEqual(item.volume.unit, self.default_volume_unit)
        self.assertEqual(item.volume.value, expected_standard_value)
        self.assertEqual(item.volume.standard, expected_standard_value)
        self.assertEqual(item.volume.cubic_meter, expected_standard_value)

    def test_update_weight(self):
        """ Test successful update of weight. """
        # Given
        expected_value = 100
        expected_standard_value = 2834.95
        item = mommy.make("Item", weight=Weight(g=99))

        # When
        serializer = ItemSerializer(item)
        serializer.update(item,
                          {"unit": "oz", "weight": expected_value})

        # Then
        item.refresh_from_db()
        self.assertEqual(item.weight.oz, expected_value)
        self.assertEqual(item.weight.unit, self.default_weight_unit)
        self.assertEqual(item.weight.value, expected_standard_value)
        self.assertEqual(item.weight.standard, expected_standard_value)
        self.assertEqual(item.weight.g, expected_standard_value)

    def test_update_unit_volume(self):
        """ Test successful update of unit volume. """
        # Given
        expected_value = 1000.0
        expected_standard_value = 1.0
        item = mommy.make("Item", volume=Volume(cubic_meter=expected_value))

        # When
        serializer = ItemSerializer(item)
        serializer.update(item, {"unit": "l"})

        # Then
        item.refresh_from_db()
        self.assertEqual(item.volume.l, expected_value)
        self.assertEqual(item.volume.unit, self.default_volume_unit)
        self.assertEqual(item.volume.value, expected_standard_value)
        self.assertEqual(item.volume.standard, expected_standard_value)
        self.assertEqual(item.volume.cubic_meter, expected_standard_value)

    def test_update_unit_weight(self):
        """ Test successful update of unit weight. """
        # Given
        expected_value = 2834.95
        expected_standard_value = 80369.415025
        item = mommy.make("Item", weight=Weight(g=expected_value))

        # When
        serializer = ItemSerializer(item)
        serializer.update(item, {"unit": "oz"})

        # Then
        item.refresh_from_db()
        self.assertEqual(item.weight.oz, expected_value)
        self.assertEqual(item.weight.unit, self.default_weight_unit)
        self.assertEqual(item.weight.value, expected_standard_value)
        self.assertEqual(item.weight.standard, expected_standard_value)
        self.assertEqual(item.weight.g, expected_standard_value)


class ItemNestedSerializerTest(TestCase):
    """ Tests for nested Item serializer. """

    def test_fields(self):
        """ Test fields for serializer. """
        # Given
        item = mommy.make("Item",
                          volume=Volume(l=1))  # noqa
        item.refresh_from_db()  # To trigger MeasurementField updates
        expected_data = {
            "id": item.id, "name": item.name,
            "unit": "cubic_meter", "volume": 0.001, "weight": None,
            "brand": {"id": item.brand.id, "name": item.brand.name}}

        # When
        serializer = ItemNestedSerializer(item)

        # Then
        self.assertEqual(loads(dumps(serializer.data)), expected_data)


class PurchaseSerializerTest(TestCase):
    """ Tests for Purchase serializer. """
    def test_fields_data(self):
        """ Test fields for serializer. """
        # Given
        purchase = mommy.make("Purchase", price=10)
        expected_data = {
            "id": purchase.id, "price": "10.000", "currency": "USD",
            "item": purchase.item.id, "order": None}

        # When
        serializer = PurchaseSerializer(purchase)

        # Then
        self.assertEqual(serializer.data, expected_data)

    def test_errors_empty(self):
        """ Test errors on empty data. """
        # Given
        expected_data = {"item": ["This field is required."]}
        data = {}

        # When
        serializer = PurchaseSerializer(data=data)
        serializer.is_valid()

        # Then
        self.assertEqual(serializer.errors, expected_data)

    def test_errors_price_empty(self):
        """ Test errors on no price data. """
        # Given
        expected_data = {"price": ["This field is required."]}
        data = {"item": mommy.make("Item").id}

        # When
        serializer = PurchaseSerializer(data=data)
        serializer.is_valid()

        # Then
        self.assertEqual(serializer.errors, expected_data)

    def test_errors_null(self):
        """ Test errors when required fields are null. """
        # Given
        expected_data = {"price": ["This field may not be null."],
                         "item": ["This field may not be null."]}
        data = {"price": None, "item": None}

        # When
        serializer = PurchaseSerializer(data=data)
        serializer.is_valid()

        # Then
        self.assertEqual(serializer.errors, expected_data)

    def test_save_no_order(self):
        """ Test successful save when order is not provided. """
        # Given
        item = mommy.make("item")
        data = {"price": 10, "item": item.id}

        # When
        serializer = PurchaseSerializer(data=data)
        serializer.is_valid()
        obj = serializer.save()

        # Then
        data = serializer.data
        obj.refresh_from_db()
        self.assertEqual(obj.price_currency, "USD")
        self.assertEqual(data.get("price"), "10.000")
        self.assertEqual(data.get("currency"), "USD")
        self.assertEqual(data.get("item"), item.id)

    def test_save_with_order(self):
        """ Test successful save when order is provided. """
        # Given
        item = mommy.make("item")
        order = mommy.make("Order")
        data = {"price": 10, "item": item.id, "order": order.id}

        # When
        serializer = PurchaseSerializer(data=data)
        serializer.is_valid()
        obj = serializer.save()

        # Then
        data = serializer.data
        obj.refresh_from_db()
        self.assertEqual(obj.price_currency, "USD")
        self.assertEqual(data.get("price"), "10.000")
        self.assertEqual(data.get("currency"), "USD")
        self.assertEqual(data.get("item"), item.id)
        self.assertEqual(data.get("order"), order.id)

    def test_save_another_currency(self):
        """ Test successful save when currency different than default one. """
        item = mommy.make("item")
        data = {"price": 10, "currency": "DOP", "item": item.id}

        # When
        serializer = PurchaseSerializer(data=data)
        serializer.is_valid()
        obj = serializer.save()

        # Then
        data = serializer.data
        obj.refresh_from_db()
        self.assertEqual(obj.price_currency, "DOP")
        self.assertEqual(data.get("price"), "10.000")
        self.assertEqual(data.get("currency"), "DOP")
        self.assertEqual(data.get("item"), item.id)


class PurchsaeNestedSerializerTest(TestCase):
    """ Tests for nested Purchase serializer. """

    def test_fields(self):
        """ Test fields for serializer. """
        # Given
        order = mommy.make("Order")
        purchase = mommy.make("Purchase",
                              price=10,
                              item__volume=Volume(l=1),  # noqa
                              order=order)
        purchase.item.refresh_from_db()  # To trigger MeasurementField updates
        expected_data = {
            "id": purchase.id, "price": "10.000", "currency": "USD",
            "item": {"id": purchase.item.id, "name": purchase.item.name,
                     "unit": "cubic_meter", "volume": 0.001, "weight": None,
                     "brand": {"id": purchase.item.brand.id,
                               "name": purchase.item.brand.name}},
            "order": {"id": order.id, "date": order.date.isoformat(),
                      "store": {"id": order.store.id,
                                "name": order.store.name}}}

        # When
        serializer = PurchaseNestedSerializer(purchase)

        # Then
        self.assertEqual(loads(dumps(serializer.data)), expected_data)
