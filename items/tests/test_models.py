""" Test for all models of items app. """
from django.test import TestCase

from schmebulock.utils import get_model_fields
from ..models import Brand, Store


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

    def test_fields(self):
        """ Test fields for model. """
        # Given
        expected_fields = ["id", "name"]

        # When
        brand = Brand()

        # Then
        self.assertEqual(get_model_fields(brand), expected_fields)


class StoreModelTest(TestCase):
    """ Tests for Store model. """

    def test_string_representation(self):
        """ Test string representation. """
        # Given
        name = "Sample store"

        # When
        store = Store(name=name)

        # Then
        self.assertEqual(str(store), name)
        self.assertEqual(str(store), store.name)

    def test_fields(self):
        """ Test fields for model. """
        # Given
        expected_fields = ["id", "name"]

        # When
        store = Store()

        # Then
        self.assertEqual(get_model_fields(store), expected_fields)
