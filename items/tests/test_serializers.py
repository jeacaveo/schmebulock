""" Test for all serializers of items app. """
from django.test import TestCase

from ..serializers import BrandSerializer, StoreSerializer


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
