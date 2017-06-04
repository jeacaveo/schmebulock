""" Tests for all views of items app. """

from model_mommy import mommy

from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from .. import models


class BrandEndpointTests(APITestCase):
    """ Test Brand endpoint.  """

    endpoint_name = "brand"
    model = models.Brand

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
    model = models.Store

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
    model = models.Order

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
