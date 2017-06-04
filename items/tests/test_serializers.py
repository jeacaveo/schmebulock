""" Test for all serializers of items app. """
from django.test import TestCase

from model_mommy import mommy

from ..serializers import (
    BrandSerializer,
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
