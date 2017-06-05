""" Test for all models of items app. """
from django.test import TestCase

from djmoney.models.fields import MoneyPatched
from measurement.measures import Weight
from model_mommy import mommy

from schmebulock.utils import get_model_fields


class ItemAppTest(TestCase):
    """ Tests for Brand model. """

    def test_app_name(self):
        """ Test name of application. """
        from ..apps import ItemsConfig
        from sys import modules
        current_module = modules[__name__]
        expected_name = "Items"

        # When
        app_config = ItemsConfig(app_name="schmebulock.items",
                                 app_module=current_module)

        # Then
        self.assertEqual(app_config.verbose_name, expected_name)


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


class ItemModelTest(TestCase):
    """ Tests for Item model. """

    def test_string_representation(self):
        """ Test string representation. """
        # When
        item = mommy.make("Item",
                          name="Blue Cheese",
                          price=MoneyPatched(50, 'DOP'),
                          weight=Weight(kg=0.500),
                          brand__name="Generic",)

        # Then
        self.assertEqual(
            str(item),
            "0.5 kg of Blue Cheese (Generic) at 50.00 DOP")

    def test_fields(self):
        """ Test fields for model. """
        # Given
        expected_fields = ["id", "name", "price_currency", "price",
                           "volume", "weight", "brand", "order"]

        # When
        item = mommy.make("Item")

        # Then
        self.assertEqual(get_model_fields(item), expected_fields)
