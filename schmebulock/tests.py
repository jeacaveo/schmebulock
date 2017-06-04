""" Test for utils under main app. """
from django.db import models
from django.test import TestCase

from schmebulock import utils


class TestModel(models.Model):
    """ Dummy model for test purposes. """
    field1 = models.IntegerField()

    class Meta:  # pylint: disable=too-few-public-methods
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
