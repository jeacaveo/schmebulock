""" Test for all serializers of items app. """
from json import dumps, loads

from django.contrib.gis.geos import GEOSGeometry
from django.test import TestCase

from measurement.measures import Volume, Weight
from model_mommy import mommy

from schmebulock.utils import get_default_fields

from ..serializers import (
    BrandSerializer,
    ItemSerializer,
    ItemNestedSerializer,
    LocationSerializer,
    LocationNestedSerializer,
    NameModelSerializer,
    OrderSerializer,
    OrderNestedSerializer,
    PurchaseSerializer,
    PurchaseNestedSerializer,
    StoreSerializer)


class NameModelSerializerTest(TestCase):
    """ Tests for generic name serializer. """

    def test_fields(self):
        """ Test fields for serializer. """
        # Given
        expected_data = {"id": None, "name": ""}

        # When
        serializer = NameModelSerializer()

        # Then
        self.assertEqual(loads(dumps(serializer.data)), expected_data)

    def test_abstract_methods(self):
        """ Test abstract methods are overriden to None. """
        # Given
        serializer = NameModelSerializer()

        # When
        create = serializer.create(None)
        update = serializer.update(None, None)

        # Then
        self.assertIsNone(create)
        self.assertIsNone(update)


class BrandSerializerTest(TestCase):
    """ Tests for Brand serializer. """

    def test_fields(self):
        """ Test fields for serializer. """
        # Given
        brand = mommy.make("Brand")
        expected_data = get_default_fields(brand)
        expected_data.update({"name": brand.name})

        # When
        serializer = BrandSerializer(brand)

        # Then
        self.assertEqual(loads(dumps(serializer.data)), expected_data)


class StoreSerializerTest(TestCase):
    """ Tests for Store serializer. """

    def test_fields(self):
        """ Test fields for serializer. """
        # Given
        brand = mommy.make("Brand")
        expected_data = get_default_fields(brand)
        expected_data.update({"name": brand.name})

        # When
        serializer = StoreSerializer(brand)

        # Then
        self.assertEqual(loads(dumps(serializer.data)), expected_data)


class OrderSerializerTest(TestCase):
    """ Tests for Order serializer. """

    def test_fields(self):
        """ Test fields for serializer. """
        # Given
        order = mommy.make("Order")
        expected_data = get_default_fields(order)
        expected_data.update({"date": order.date.isoformat(),
                              "store": order.store.id})

        # When
        serializer = OrderSerializer(order)

        # Then
        self.assertEqual(loads(dumps(serializer.data)), expected_data)


class OrderNestedSerializerTest(TestCase):
    """ Tests for nested Order serializer. """

    def test_fields(self):
        """ Test fields for serializer. """
        # Given
        order = mommy.make("Order")
        expected_data = get_default_fields(order)
        expected_data.update({"date": order.date.isoformat(),
                              "store": {"id": order.store.id,
                                        "name": order.store.name}})

        # When
        serializer = OrderNestedSerializer(order)

        # Then
        self.assertEqual(loads(dumps(serializer.data)), expected_data)


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
        expected_data = get_default_fields(item)
        expected_data.update({
            "name": item.name, "brand": item.brand.id,
            "unit": self.default_volume_unit, "volume": 0.001, "weight": 1.0})

        # When
        serializer = ItemSerializer(item)

        # Then
        self.assertEqual(loads(dumps(serializer.data)), expected_data)

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
        expected_data = get_default_fields(item)
        expected_data.update({
            "name": item.name,
            "unit": "cubic_meter", "volume": 0.001, "weight": None,
            "brand": {"id": item.brand.id, "name": item.brand.name}})

        # When
        serializer = ItemNestedSerializer(item)

        # Then
        self.assertEqual(loads(dumps(serializer.data)), expected_data)


class LocationSerializerTest(TestCase):
    """ Tests for Location serializer. """

    def setUp(self):
        self.location = GEOSGeometry('POINT(0.00 0.00)')

    def test_fields_data(self):
        """ Test fields for serializer. """
        # Given
        location = mommy.make("Location",
                              district__city__location=self.location,
                              district__location=self.location)
        expected_data = get_default_fields(location)
        expected_data.update({"address": location.address,
                              "district": location.district.id})

        # When
        serializer = LocationSerializer(location)

        # Then
        self.assertEqual(serializer.data, expected_data)

    def test_errors_empty(self):
        """ Test errors on empty data. """
        # Given
        expected_data = {"address": ["This field is required."],
                         "district": ["This field is required."]}
        data = {}

        # When
        serializer = LocationSerializer(data=data)
        serializer.is_valid()

        # Then
        self.assertEqual(serializer.errors, expected_data)

    def test_errors_null(self):
        """ Test errors when required fields are null. """
        # Given
        expected_data = {"address": ["This field may not be null."],
                         "district": ["This field may not be null."]}
        data = {"address": None, "district": None}

        # When
        serializer = LocationSerializer(data=data)
        serializer.is_valid()

        # Then
        self.assertEqual(serializer.errors, expected_data)


class LocationNestedSerializerTest(TestCase):
    """ Tests for nested Location serializer. """

    def setUp(self):
        self.location = GEOSGeometry('POINT(0.00 0.00)')

    def test_fields(self):
        """ Test fields for serializer. """
        # Given
        location = mommy.make("Location",
                              district__city__location=self.location,
                              district__location=self.location)
        district = location.district
        city = district.city
        country = city.country
        expected_data = get_default_fields(location)
        expected_data.update({
            "address": location.address,
            "district": {"id": district.id,
                         "name": district.name,
                         "city": {"id": city.id,
                                  "name": city.name,
                                  "country": {"id": country.id,
                                              "name": country.name}}}})

        # When
        serializer = LocationNestedSerializer(location)

        # Then
        self.assertEqual(loads(dumps(serializer.data)), expected_data)


class PurchaseSerializerTest(TestCase):
    """ Tests for Purchase serializer. """

    def setUp(self):
        point = GEOSGeometry('POINT(0.00 0.00)')
        self.location = mommy.make("Location",
                                   district__city__location=point,
                                   district__location=point)

    def test_fields_data(self):
        """ Test fields for serializer. """
        # Given
        purchase = mommy.make("Purchase", price=10, location=self.location)
        expected_data = get_default_fields(purchase)
        expected_data.update({"price": "10.000", "currency": "USD",
                              "item": purchase.item.id, "order": None,
                              "location": self.location.id})

        # When
        serializer = PurchaseSerializer(purchase)

        # Then
        self.assertEqual(serializer.data, expected_data)

    def test_errors_empty(self):
        """ Test errors on empty data. """
        # Given
        expected_data = {"item": ["This field is required."],
                         "location": ["This field is required."]}
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
        data = {"item": mommy.make("Item").id, "location": self.location.id}

        # When
        serializer = PurchaseSerializer(data=data)
        serializer.is_valid()

        # Then
        self.assertEqual(serializer.errors, expected_data)

    def test_errors_null(self):
        """ Test errors when required fields are null. """
        # Given
        expected_data = {"price": ["This field may not be null."],
                         "item": ["This field may not be null."],
                         "location": ["This field may not be null."]}
        data = {"price": None, "item": None, "location": None}

        # When
        serializer = PurchaseSerializer(data=data)
        serializer.is_valid()

        # Then
        self.assertEqual(serializer.errors, expected_data)

    def test_save_no_order(self):
        """ Test successful save when order is not provided. """
        # Given
        item = mommy.make("item")
        data = {"price": 10, "item": item.id, "location": self.location.id}

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
        data = {"price": 10, "item": item.id, "order": order.id,
                "location": self.location.id}

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
        data = {"price": 10, "currency": "DOP", "item": item.id,
                "location": self.location.id}

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

    def test_errors_invalid_currency(self):
        """ Test error when invalid currency is provided. """
        # Given
        item = mommy.make("item")
        expected_data = {
            "currency": ["'invalid_currency' is an invalid currency code."]}
        data = {"price": 10, "currency": "invalid_currency", "item": item.id,
                "location": self.location.id}

        # When
        serializer = PurchaseSerializer(data=data)
        serializer.is_valid()

        # Then
        self.assertEqual(serializer.errors, expected_data)


class PurchaseNestedSerializerTest(TestCase):
    """ Tests for nested Purchase serializer. """

    def setUp(self):
        point = GEOSGeometry('POINT(0.00 0.00)')
        self.location = mommy.make("Location",
                                   address="Address",
                                   district__name="District",
                                   district__city__name="City",
                                   district__city__location=point,
                                   district__city__country__name="Country",
                                   district__location=point)

    def test_fields(self):
        """ Test fields for serializer. """
        # Given
        order = mommy.make("Order")
        purchase = mommy.make("Purchase",
                              price=10,
                              item__volume=Volume(l=1),  # noqa
                              order=order,
                              location=self.location)
        purchase.item.refresh_from_db()  # To trigger MeasurementField updates
        expected_data = get_default_fields(purchase)
        expected_data.update({
            "price": "10.000", "currency": "USD",
            "item": {"id": purchase.item.id, "name": purchase.item.name,
                     "unit": "cubic_meter", "volume": 0.001, "weight": None,
                     "brand": {"id": purchase.item.brand.id,
                               "name": purchase.item.brand.name}},
            "order": {"id": order.id, "date": order.date.isoformat(),
                      "store": {"id": order.store.id,
                                "name": order.store.name}},
            "location": "Address, District, City, Country"})

        # When
        serializer = PurchaseNestedSerializer(purchase)

        # Then
        self.assertEqual(loads(dumps(serializer.data)), expected_data)
