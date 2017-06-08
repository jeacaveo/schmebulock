""" Test for utils under main app. """
from collections import OrderedDict

from django.db import models
from django.test import TestCase

from schmebulock import utils


class TestModel(models.Model):
    """ Dummy model for test purposes. """
    field1 = models.IntegerField()

    class Meta:
        """ Assigning an app_label just to make it run. """
        app_label = "schmebulock"


class GetModelFieldsTest(TestCase):
    """ Tests get_model_fields function. """

    def test_function(self):
        """ Test successful call to function. """
        # Given
        model = TestModel()

        # When
        fields = utils.get_model_fields(model)

        # Then
        self.assertEqual(fields, ['id', 'field1'])


class GetChoicesTest(TestCase):
    """ Tests get_choices function. """

    def setUp(self):
        """ Data for all the tests. """
        self.data = OrderedDict([("key1", "val1"), ("key2", "val2")])

    def test_function(self):
        """ Test successful call to function with only required parameters. """
        # Given
        expected_choices = [("val1", "key1"), ("val2", "key2")]

        # When
        choices = utils.get_choices(self.data)

        # Then
        self.assertEqual(choices, expected_choices)

    def test_non_ordered_dict(self):
        """ Test successful call to function with non OrderedDict. """
        # Given
        data = {"key1": "val1"}
        expected_choices = [("val1", "key1")]

        # When
        choices = utils.get_choices(data)

        # Then
        self.assertEqual(choices, expected_choices)

    def test_first(self):
        """ Test successful call to function with first parameter. """
        # Given
        expected_choices = [("val2", "key2"), ("val1", "key1")]

        # When
        choices = utils.get_choices(self.data, first="key2")

        # Then
        self.assertEqual(choices, expected_choices)

    def test_first_invalid_value(self):
        """
        Test successful call to function with an invalid first parameter.

        """
        # Given
        expected_choices = [("val1", "key1"), ("val2", "key2")]

        # When
        choices = utils.get_choices(self.data, first="invalid_key")

        # Then
        self.assertEqual(choices, expected_choices)
