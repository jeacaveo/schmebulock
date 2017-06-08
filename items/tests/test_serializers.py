""" Test for all serializers of items app. """
from django.test import TestCase

from model_mommy import mommy

from ..serializers import (
    BrandSerializer,
    ItemSerializer,
    OrderSerializer,
    OrderNestedSerializer,
    StoreSerializer,
    )


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

    def test_fields(self):
        """ Test fields for serializer. """
        # Given
        item = mommy.make("Item", price=10)
        expected_data = {
            "id": item.id, "name": item.name, "price": "10.000",
            "currency": item.price_currency, "volume": None, "weight": None,
            "brand": item.brand.id, "order": item.order.id}

        # When
        serializer = ItemSerializer(item)

        # Then
        self.assertEqual(serializer.data, expected_data)

    def test_errors_empty(self):
        """ Test errors on empty data. """
        # Given
        expected_data = {"name": ["This field is required."],
                         "unit": ["This field is required."],
                         "brand": ["This field is required."],
                         "order": ["This field is required."]}
        data = {}

        # When
        serializer = ItemSerializer(data=data)
        serializer.is_valid()

        # Then
        self.assertEqual(serializer.errors, expected_data)

    def test_errors_no_price(self):
        """ Test errors when price is not provided. """
        # Given
        brand = mommy.make("Brand")
        order = mommy.make("Order")
        expected_data = {"price": ["This field is required."]}
        data = {"name": "Item X", "unit": "g",
                "brand": brand.id, "order": order.id}

        # When
        serializer = ItemSerializer(data=data)
        serializer.is_valid()

        # Then
        self.assertEqual(serializer.errors, expected_data)

    def test_errors_null(self):
        """ Test errors when required fields are null. """
        # Given
        expected_data = {"name": ["This field may not be null."],
                         "price": ["This field may not be null."],
                         "unit": ["This field may not be null."],
                         "brand": ["This field may not be null."],
                         "order": ["This field may not be null."]}
        data = {"name": None, "price": None, "unit": None,
                "brand": None, "order": None}

        # When
        serializer = ItemSerializer(data=data)
        serializer.is_valid()

        # Then
        self.assertEqual(serializer.errors, expected_data)

    def test_errors_no_volume_weight(self):
        """ Test errors when both volume and weight fields are not provided. """
        # Given
        brand = mommy.make("Brand")
        order = mommy.make("Order")
        expected_data = {"volume": ["This field is required if "
                                    "'weight' is not available."],
                         "weight": ["This field is required if "
                                    "'volume' is not available."]}
        data = {"name": "Item X", "price": 10, "unit": "g",
                "brand": brand.id, "order": order.id}

        # When
        serializer = ItemSerializer(data=data)
        serializer.is_valid()

        # Then
        self.assertEqual(serializer.errors, expected_data)

    def test_errors_both_volume_weight(self):
        """ Test errors when both volume and weight fields are provided. """
        # Given
        brand = mommy.make("Brand")
        order = mommy.make("Order")
        expected_data = {
            "non_field_errors": ["Either 'volume' or 'weight' must be "
                                 "provided, not both."]}
        data = {"name": "Item X", "price": 10, "unit": "g",
                "volume": 100, "weight": 100,
                "brand": brand.id, "order": order.id}

        # When
        serializer = ItemSerializer(data=data)
        serializer.is_valid()

        # Then
        self.assertEqual(serializer.errors, expected_data)

    def test_errors_invalid_volume_unit(self):
        """ Test errors when volume is provided with an invalid unit. """
        # Given
        brand = mommy.make("Brand")
        order = mommy.make("Order")
        expected_data = {
            "unit": ["'invalid_unit' is an invalid unit for volume field."]}
        data = {"name": "Item X", "price": 10, "volume": 100,
                "unit": "invalid_unit", "brand": brand.id, "order": order.id}

        # When
        serializer = ItemSerializer(data=data)
        serializer.is_valid()

        # Then
        self.assertEqual(serializer.errors, expected_data)

    def test_errors_invalid_weight_unit(self):
        """ Test errors when weight is provided with an invalid unit. """
        # Given
        brand = mommy.make("Brand")
        order = mommy.make("Order")
        expected_data = {
            "unit": ["'invalid_unit' is an invalid unit for weight field."]}
        data = {"name": "Item X", "price": 10, "weight": 100,
                "unit": "invalid_unit", "brand": brand.id, "order": order.id}

        # When
        serializer = ItemSerializer(data=data)
        serializer.is_valid()

        # Then
        self.assertEqual(serializer.errors, expected_data)

    def test_save_volume(self):
        """ Test successful save when volume is provided. """
        # Given
        brand = mommy.make("Brand")
        order = mommy.make("Order")
        data = {"name": "Item X", "price": 10, "volume": 100, "unit": "l",
                "brand": brand.id, "order": order.id}

        # When
        serializer = ItemSerializer(data=data)
        serializer.is_valid()
        obj = serializer.save()

        # Then
        self.assertEqual(str(obj.price.amount), "10.000")
        self.assertEqual(obj.price_currency, "USD")
        self.assertEqual(str(obj.volume), "100.0")
        self.assertEqual(obj.brand, brand)
        self.assertEqual(obj.order, order)

    def test_save_weight(self):
        """ Test successful save when weight is provided. """
        # Given
        brand = mommy.make("Brand")
        order = mommy.make("Order")
        data = {"name": "Item X", "price": 10, "weight": 100, "unit": "g",
                "brand": brand.id, "order": order.id}

        # When
        serializer = ItemSerializer(data=data)
        serializer.is_valid()
        obj = serializer.save()

        # Then
        self.assertEqual(str(obj.price.amount), "10.000")
        self.assertEqual(obj.price_currency, "USD")
        self.assertEqual(str(obj.weight), "100.0")
        self.assertEqual(obj.brand, brand)
        self.assertEqual(obj.order, order)
