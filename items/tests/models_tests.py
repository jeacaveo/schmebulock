""" Test for all models of items app. """
from django.test import TestCase

from ..models import Brand


class BrandModelTest(TestCase):
    """ Tests for Brand model. """

    def test_string_representation(self):
        """ Test string representation. """
        # Given
        name = "Sample brand"

        # When
        brand = Brand(name=name)

        # Then
        self.assertEqual(str(brand), name)
        self.assertEqual(str(brand), brand.name)

    def test_model_fields(self):
        """ Test fields for model. """
        # Given
        expected_fields = ["id", "name"]

        # When
        brand = Brand()

        # Then
        self.assertEqual(brand, expected_fields)
