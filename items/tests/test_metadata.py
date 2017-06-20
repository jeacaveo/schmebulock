""" Test for all metadata of items app. """
from django.test import TestCase

from ..metadata import CustomItemMetadata, CustomPurchaseMetadata
from ..serializers import ItemSerializer, PurchaseSerializer


class CustomItemMetadataTest(TestCase):
    """ Tests for CustomItemMetadata. """

    def test_unit_choices_volume(self):
        """ Test get_field_info for volume returns unit_choices. """
        # Given
        expected_choice = ("cubic_meter", "cubic meter")
        field = dict(ItemSerializer().fields.items())["volume"]

        # When
        metadata = CustomItemMetadata()
        result = metadata.get_field_info(field)

        # Then
        self.assertEqual(result.get("unit_choices")[0], expected_choice)

    def test_unit_choices_weight(self):
        """ Test get_field_info for weight returns unit_choices. """
        # Given
        expected_choice = ("g", "gram")
        field = dict(ItemSerializer().fields.items())["weight"]

        # When
        metadata = CustomItemMetadata()
        result = metadata.get_field_info(field)

        # Then
        self.assertEqual(result.get("unit_choices")[0], expected_choice)

    def test_normal_functionality(self):
        """ Test get_field_info for non volume/weight returns expected. """
        # Given
        field = dict(ItemSerializer().fields.items())["name"]

        # When
        metadata = CustomItemMetadata()
        result = metadata.get_field_info(field)

        # Then
        self.assertEqual(result.get("unit_choices"), None)


class CustomPurchaseMetadataTest(TestCase):
    """ Tests for CustomPurchaseMetadata. """

    def test_unit_choices_volume(self):
        """ Test get_field_info for currency returns choices. """
        # Given
        expected_choice = ("USD", "US Dollar")
        field = dict(PurchaseSerializer().fields.items())["currency"]

        # When
        metadata = CustomPurchaseMetadata()
        result = metadata.get_field_info(field)

        # Then
        self.assertEqual(result.get("choices")[168], expected_choice)

    def test_normal_functionality(self):
        """ Test get_field_info for non volume/weight returns expected. """
        # Given
        field = dict(PurchaseSerializer().fields.items())["price"]

        # When
        metadata = CustomPurchaseMetadata()
        result = metadata.get_field_info(field)

        # Then
        self.assertEqual(result.get("choices"), None)
