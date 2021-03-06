""" Tests for all views of items app. """
from django.contrib.gis.geos import GEOSGeometry

from model_mommy import mommy

from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APIClient, APITestCase

from schmebulock.utils import get_default_fields


def get_authentication_token():
    """
    Get JWT token.

    Returns:
        string, JWT token.

    """
    password = "admin"
    user = mommy.make("User", username="admin")
    user.set_password(password)
    user.save()
    response = APIClient().post(
        "/api/auth/token/",
        {"username": user.username, "password": password},
        format='json')
    return response.data.get("token")


class BrandEndpointTests(APITestCase):
    """ Test Brand endpoint.  """

    endpoint_name = "brand"

    def setUp(self):
        """ Setup for tests. """
        self.client = APIClient()
        self.client.credentials(
            HTTP_AUTHORIZATION="Bearer {0}".format(
                get_authentication_token()))

    def test_get_list_empty(self):
        """ Test GET list/all returns expected when no data available. """
        # Given
        expected_data = []
        url = reverse("{}-list".format(self.endpoint_name))

        # When
        response = self.client.get(url)

        # Then
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()["results"], expected_data)

    def test_get_list(self):
        """ Test GET list/all expected results when data available. """
        # Given
        brand = mommy.make("Brand")
        expected_data = get_default_fields(brand)
        expected_data.update({"name": brand.name})
        url = reverse("{}-list".format(self.endpoint_name))

        # When
        response = self.client.get(url)
        data = response.json()["results"]

        # Then
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0], expected_data)


class StoreEndpointTests(APITestCase):
    """ Test Store endpoint.  """

    endpoint_name = "store"

    def setUp(self):
        """ Setup for tests. """
        self.client = APIClient()
        self.client.credentials(
            HTTP_AUTHORIZATION="Bearer {0}".format(
                get_authentication_token()))

    def test_get_list_empty(self):
        """ Test GET list/all returns expected when no data available. """
        # Given
        expected_data = []
        url = reverse("{}-list".format(self.endpoint_name))

        # When
        response = self.client.get(url)

        # Then
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()["results"], expected_data)

    def test_get_list(self):
        """ Test GET list/all expected results when data available. """
        # Given
        store = mommy.make("Store")
        expected_data = get_default_fields(store)
        expected_data.update({"name": store.name})
        url = reverse("{}-list".format(self.endpoint_name))

        # When
        response = self.client.get(url)
        data = response.json()["results"]

        # Then
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0], expected_data)


class OrderEndpointTests(APITestCase):
    """ Test Order endpoint.  """

    endpoint_name = "order"

    def setUp(self):
        """ Setup for tests. """
        self.client = APIClient()
        self.client.credentials(
            HTTP_AUTHORIZATION="Bearer {0}".format(
                get_authentication_token()))

    def test_get_list_empty(self):
        """ Test GET list/all returns expected when no data available. """
        # Given
        expected_data = []
        url = reverse("{}-list".format(self.endpoint_name))

        # When
        response = self.client.get(url)

        # Then
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()["results"], expected_data)

    def test_get_list(self):
        """ Test GET list/all expected results when data available. """
        # Given
        order = mommy.make("Order")
        expected_data = get_default_fields(order)
        expected_data.update({"date": order.date.isoformat(),
                              "store": order.store.id})
        url = reverse("{}-list".format(self.endpoint_name))

        # When
        response = self.client.get(url)
        data = response.json()["results"]

        # Then
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0], expected_data)

    def test_get_detail_nested(self):
        """ Test GET detail nested returns nested data. """
        # Given
        order = mommy.make("Order")
        expected_data = get_default_fields(order)
        expected_data.update({"date": order.date.isoformat(),
                              "store": {"id": order.store.id,
                                        "name": order.store.name}})
        url = reverse("{}-detail".format(self.endpoint_name),
                      args=[order.id])

        # When
        response = self.client.get(url, data={"nested": True})

        # Then
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), expected_data)


class ItemEndpointTests(APITestCase):
    """ Test Item endpoint.  """

    endpoint_name = "item"

    def setUp(self):
        """ Setup for tests. """
        self.client = APIClient()
        self.client.credentials(
            HTTP_AUTHORIZATION="Bearer {0}".format(
                get_authentication_token()))

    def test_get_list_empty(self):
        """ Test GET list/all returns expected when no data available. """
        # Given
        expected_data = []
        url = reverse("{}-list".format(self.endpoint_name))

        # When
        response = self.client.get(url)

        # Then
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()["results"], expected_data)

    def test_get_list(self):
        """ Test GET list/all expected results when data available. """
        # Given
        item = mommy.make("Item")
        expected_data = get_default_fields(item)
        expected_data.update({"name": item.name,
                              "unit": None,
                              "volume": None,
                              "weight": None,
                              "brand": item.brand.id})
        url = reverse("{}-list".format(self.endpoint_name))

        # When
        response = self.client.get(url)
        data = response.json()["results"]

        # Then
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0], expected_data)

    def test_get_detail_nested(self):
        """ Test GET detail nested returns nested data. """
        # Given
        item = mommy.make("Item")
        expected_data = get_default_fields(item)
        expected_data.update({
            "name": item.name,
            "unit": None,
            "volume": None,
            "weight": None,
            "brand": {"id": item.brand.id, "name": item.brand.name}})
        url = reverse("{}-detail".format(self.endpoint_name),
                      args=[item.id])

        # When
        response = self.client.get(url, data={"nested": True})

        # Then
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), expected_data)


class LocationEndpointTests(APITestCase):
    """ Test Location endpoint.  """

    endpoint_name = "location"

    def setUp(self):
        """ Setup for tests. """
        self.client = APIClient()
        self.client.credentials(
            HTTP_AUTHORIZATION="Bearer {0}".format(
                get_authentication_token()))
        self.point = GEOSGeometry('POINT(0.00 0.00)')

    def test_get_list_empty(self):
        """ Test GET list/all returns expected when no data available. """
        # Given
        expected_data = []
        url = reverse("{}-list".format(self.endpoint_name))

        # When
        response = self.client.get(url)

        # Then
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()["results"], expected_data)

    def test_get_list(self):
        """ Test GET list/all expected results when data available. """
        # Given
        location = mommy.make("Location",
                              district__city__location=self.point,
                              district__location=self.point)
        expected_data = get_default_fields(location)
        expected_data.update({"address": location.address,
                              "district": location.district.id})
        url = reverse("{}-list".format(self.endpoint_name))

        # When
        response = self.client.get(url)
        data = response.json()["results"]

        # Then
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0], expected_data)

    def test_get_detail_nested(self):
        """ Test GET detail nested returns nested data. """
        # Given
        location = mommy.make("Location",
                              district__city__location=self.point,
                              district__location=self.point)
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
        url = reverse("{}-detail".format(self.endpoint_name),
                      args=[location.id])

        # When
        response = self.client.get(url, data={"nested": True})

        # Then
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), expected_data)


class PurchaseEndpointTests(APITestCase):
    """ Test Purchse endpoint.  """

    endpoint_name = "purchase"

    def setUp(self):
        """ Setup for tests. """
        self.client = APIClient()
        self.client.credentials(
            HTTP_AUTHORIZATION="Bearer {0}".format(
                get_authentication_token()))
        point = GEOSGeometry('POINT(0.00 0.00)')
        self.location = mommy.make("Location",
                                   address="Address",
                                   district__name="District",
                                   district__city__name="City",
                                   district__city__location=point,
                                   district__city__country__name="Country",
                                   district__location=point)

    def test_get_list_empty(self):
        """ Test GET list/all returns expected when no data available. """
        # Given
        expected_data = []
        url = reverse("{}-list".format(self.endpoint_name))

        # When
        response = self.client.get(url)

        # Then
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()["results"], expected_data)

    def test_get_list(self):
        """ Test GET list/all expected results when data available. """
        # Given
        purchase = mommy.make("Purchase", price=10, location=self.location)
        expected_data = get_default_fields(purchase)
        expected_data.update({"price": "10.000",
                              "currency": "USD",
                              "item": purchase.item.id,
                              "order": None,
                              "location": self.location.id})
        url = reverse("{}-list".format(self.endpoint_name))

        # When
        response = self.client.get(url)
        data = response.json()["results"]

        # Then
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0], expected_data)

    def test_get_detail_nested(self):
        """ Test GET detail nested returns nested data. """
        # Given
        order = mommy.make("Order")
        purchase = mommy.make("Purchase",
                              price=10, order=order, location=self.location)
        expected_data = get_default_fields(purchase)
        expected_data.update({
            "price": "10.000", "currency": "USD",
            "item": {"id": purchase.item.id, "name": purchase.item.name,
                     "unit": None, "volume": None, "weight": None,
                     "brand": {"id": purchase.item.brand.id,
                               "name": purchase.item.brand.name}},
            "order": {"id": order.id, "date": order.date.isoformat(),
                      "store": {"id": order.store.id,
                                "name": order.store.name}},
            "location": "Address, District, City, Country"})
        url = reverse("{}-detail".format(self.endpoint_name),
                      args=[purchase.id])

        # When
        response = self.client.get(url, data={"nested": True})

        # Then
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), expected_data)
