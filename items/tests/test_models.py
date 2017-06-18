""" Test for all models of items app. """
from django.contrib.gis.geos import GEOSGeometry
from django.test import TestCase

from djmoney.models.fields import MoneyPatched
from measurement.measures import Weight
from model_mommy import mommy

from schmebulock.utils import get_model_fields


DEFAULT_FIELDS = ["id",
                  "created_by", "created_with_session_key",
                  "modified_by", "modified_with_session_key",
                  "created", "modified"]


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
        expected_fields = DEFAULT_FIELDS + ["name"]

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
        expected_fields = DEFAULT_FIELDS + ["name"]

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
        expected_fields = DEFAULT_FIELDS + ["date", "store"]

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
                          weight=Weight(kg=0.500),
                          brand__name="Generic",)

        # Then
        self.assertEqual(
            str(item),
            "Blue Cheese (Generic), 0.5 kg")

    def test_fields(self):
        """ Test fields for model. """
        # Given
        expected_fields = DEFAULT_FIELDS + [
            "name", "volume", "weight", "brand"]

        # When
        item = mommy.make("Item")

        # Then
        self.assertEqual(get_model_fields(item), expected_fields)


class LocationModelTest(TestCase):
    """ Tests for Location model. """

    def setUp(self):
        self.point = GEOSGeometry('POINT(0.00 0.00)')

    def test_string_representation(self):
        """ Test string representation. """
        # When
        location = mommy.make("Location",
                              address="Address",
                              district__name="District",
                              district__city__name="City",
                              district__city__location=self.point,
                              district__city__country__name="Country",
                              district__location=self.point)

        # Then
        self.assertEqual(str(location), "Address, District, City, Country")

    def test_fields(self):
        """ Test fields for model. """
        # Given
        expected_fields = DEFAULT_FIELDS + ["address", "district"]

        # When
        location = mommy.make("Location",
                              district__city__location=self.point,
                              district__location=self.point)

        # Then
        self.assertEqual(get_model_fields(location), expected_fields)


class PurchaseModelTest(TestCase):
    """ Tests for Purchase model. """

    def setUp(self):
        point = GEOSGeometry('POINT(0.00 0.00)')
        self.location = mommy.make("Location",
                                   district__city__location=point,
                                   district__location=point)

    def test_string_representation(self):
        """ Test string representation. """
        # When
        purchase = mommy.make("Purchase",
                              price=MoneyPatched(50, "DOP"),
                              item__name="Blue Cheese",
                              item__weight=Weight(kg=0.500),
                              item__brand__name="Generic",
                              order__id=999,
                              location=self.location)

        # Then
        self.assertEqual(
            str(purchase),
            "Blue Cheese (Generic), 0.5 kg at 50.00 DOP - #999")

    def test_string_repr_no_order(self):
        """ Test string representation when order is empty. """
        # When
        purchase = mommy.make("Purchase",
                              price=MoneyPatched(50, "DOP"),
                              item__name="Blue Cheese",
                              item__weight=Weight(kg=0.500),
                              item__brand__name="Generic",
                              order=None,
                              location=self.location)

        # Then
        self.assertEqual(
            str(purchase),
            "Blue Cheese (Generic), 0.5 kg at 50.00 DOP - #N/A")

    def test_fields(self):
        """ Test fields for model. """
        # Given
        expected_fields = DEFAULT_FIELDS + [
            "price_currency", "price", "item", "location", "order"]

        # When
        purchase = mommy.make("Purchase", location=self.location)

        # Then
        self.assertEqual(get_model_fields(purchase), expected_fields)
