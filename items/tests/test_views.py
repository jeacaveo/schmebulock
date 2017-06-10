""" Tests for all views of items app. """

from model_mommy import mommy

from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase


class BrandEndpointTests(APITestCase):
    """ Test Brand endpoint.  """

    endpoint_name = "brand"

    def test_get_list_empty(self):
        """ Test GET list/all returns expected when no data available. """
        # Given
        expected_data = []
        url = reverse("{}-list".format(self.endpoint_name))

        # When
        response = self.client.get(url)

        # Then
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), expected_data)

    def test_get_list(self):
        """ Test GET list/all expected results when data available. """
        # Given
        brand = mommy.make("Brand")
        expected_data = {"id": brand.id, "name": brand.name}
        url = reverse("{}-list".format(self.endpoint_name))

        # When
        response = self.client.get(url)
        data = response.json()

        # Then
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0], expected_data)


class StoreEndpointTests(APITestCase):
    """ Test Store endpoint.  """

    endpoint_name = "store"

    def test_get_list_empty(self):
        """ Test GET list/all returns expected when no data available. """
        # Given
        expected_data = []
        url = reverse("{}-list".format(self.endpoint_name))

        # When
        response = self.client.get(url)

        # Then
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), expected_data)

    def test_get_list(self):
        """ Test GET list/all expected results when data available. """
        # Given
        store = mommy.make("Store")
        expected_data = {"id": store.id, "name": store.name}
        url = reverse("{}-list".format(self.endpoint_name))

        # When
        response = self.client.get(url)
        data = response.json()

        # Then
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0], expected_data)


class OrderEndpointTests(APITestCase):
    """ Test Order endpoint.  """

    endpoint_name = "order"

    def test_get_list_empty(self):
        """ Test GET list/all returns expected when no data available. """
        # Given
        expected_data = []
        url = reverse("{}-list".format(self.endpoint_name))

        # When
        response = self.client.get(url)

        # Then
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), expected_data)

    def test_get_list(self):
        """ Test GET list/all expected results when data available. """
        # Given
        order = mommy.make("Order")
        expected_data = {"id": order.id,
                         "date": order.date.isoformat(),
                         "store": order.store.id}
        url = reverse("{}-list".format(self.endpoint_name))

        # When
        response = self.client.get(url)
        data = response.json()

        # Then
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0], expected_data)

    def test_get_detail_nested(self):
        """ Test GET detail nested returns nested data. """
        # Given
        order = mommy.make("Order")
        expected_data = {"id": order.id,
                         "date": order.date.isoformat(),
                         "store": {"id": order.store.id,
                                   "name": order.store.name}}
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

    def test_get_list_empty(self):
        """ Test GET list/all returns expected when no data available. """
        # Given
        expected_data = []
        url = reverse("{}-list".format(self.endpoint_name))

        # When
        response = self.client.get(url)

        # Then
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), expected_data)

    def test_get_list(self):
        """ Test GET list/all expected results when data available. """
        # Given
        item = mommy.make("Item")
        expected_data = {"id": item.id,
                         "name": item.name,
                         "unit": None,
                         "volume": None,
                         "weight": None,
                         "brand": item.brand.id}
        url = reverse("{}-list".format(self.endpoint_name))

        # When
        response = self.client.get(url)
        data = response.json()

        # Then
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0], expected_data)

    def test_get_detail_nested(self):
        """ Test GET detail nested returns nested data. """
        # Given
        item = mommy.make("Item")
        expected_data = {
            "id": item.id,
            "name": item.name,
            "unit": None,
            "volume": None,
            "weight": None,
            "brand": {"id": item.brand.id, "name": item.brand.name}}
        url = reverse("{}-detail".format(self.endpoint_name),
                      args=[item.id])

        # When
        response = self.client.get(url, data={"nested": True})

        # Then
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), expected_data)


class PurchaseEndpointTests(APITestCase):
    """ Test Purchse endpoint.  """

    endpoint_name = "purchase"

    def test_get_list_empty(self):
        """ Test GET list/all returns expected when no data available. """
        # Given
        expected_data = []
        url = reverse("{}-list".format(self.endpoint_name))

        # When
        response = self.client.get(url)

        # Then
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), expected_data)

    def test_get_list(self):
        """ Test GET list/all expected results when data available. """
        # Given
        purchase = mommy.make("Purchase", price=10)
        expected_data = {"id": purchase.id,
                         "price": "10.000",
                         "currency": "USD",
                         "item": purchase.item.id,
                         "order": None}
        url = reverse("{}-list".format(self.endpoint_name))

        # When
        response = self.client.get(url)
        data = response.json()

        # Then
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0], expected_data)

    def test_get_detail_nested(self):
        """ Test GET detail nested returns nested data. """
        # Given
        order = mommy.make("Order")
        purchase = mommy.make("Purchase", price=10, order=order)
        expected_data = {
            "id": purchase.id, "price": "10.000", "currency": "USD",
            "item": {"id": purchase.item.id, "name": purchase.item.name,
                     "unit": None, "volume": None, "weight": None,
                     "brand": {"id": purchase.item.brand.id,
                               "name": purchase.item.brand.name}},
            "order": {"id": order.id, "date": order.date.isoformat(),
                      "store": {"id": order.store.id,
                                "name": order.store.name}}}
        url = reverse("{}-detail".format(self.endpoint_name),
                      args=[purchase.id])

        # When
        response = self.client.get(url, data={"nested": True})

        # Then
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), expected_data)
