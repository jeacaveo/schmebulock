""" Tests for all views of items app. """

from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from .. import models


class BrandEndpointBasicTests(APITestCase):
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
        self.assertEqual(response.data, expected_data)

    def test_get_list(self):
        """ Test GET list/all expected results when data available. """
        # Given
        expected_name = "Brand name"
        expected_data = {"id": 1, "name": expected_name}
        url = reverse("{}-list".format(self.endpoint_name))
        models.Brand.objects.create(name=expected_name)

        # When
        response = self.client.get(url)
        data = response.data

        # Then
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0], expected_data)
        self.assertEqual(data[0].get("name"), expected_name)
