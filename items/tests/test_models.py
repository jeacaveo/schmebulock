""" Test for all models of items app. """
from django.test import TestCase

from model_mommy import mommy

from schmebulock.utils import get_model_fields


class BrandModelTest(TestCase):
    """ Tests for Brand model. """

    def test_string_representation(self):
        """ Test string representation. """
        # Given
        name = "Sample brand"

        # When
        brand = mommy.make("Brand", name=name)

        # Then
        self.assertEqual(str(brand), name)
        self.assertEqual(str(brand), brand.name)

    def test_fields(self):
        """ Test fields for model. """
        # Given
        expected_fields = ["id", "name"]

        # When
        brand = mommy.make("Brand")

        # Then
        self.assertEqual(get_model_fields(brand), expected_fields)


class StoreModelTest(TestCase):
    """ Tests for Store model. """

    def test_string_representation(self):
        """ Test string representation. """
        # Given
        name = "Sample store"

        # When
        store = mommy.make("Store", name=name)

        # Then
        self.assertEqual(str(store), name)
        self.assertEqual(str(store), store.name)

    def test_fields(self):
        """ Test fields for model. """
        # Given
        expected_fields = ["id", "name"]

        # When
        store = mommy.make("Store")

        # Then
        self.assertEqual(get_model_fields(store), expected_fields)


class OrderModelTest(TestCase):
    """ Tests for Order model. """

    def test_string_representation(self):
        """ Test string representation. """
        # When
        order = mommy.make("Order")

        # Then
        self.assertEqual(str(order), "{} - {}".format(
            order.store.name, order.date))

    def test_fields(self):
        """ Test fields for model. """
        # Given
        expected_fields = ["id", "date", "store"]

        # When
        order = mommy.make("Order")

        # Then
        self.assertEqual(get_model_fields(order), expected_fields)
