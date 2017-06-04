""" Models for items app. """
from django.db import models


class Brand(models.Model):
    """ Representation of a brand (IKEA, Pampers, etc.). """
    name = models.CharField(max_length=128)

    def __str__(self):
        """ String representation for model. """
        return self.name


class Store(models.Model):
    """ Representation of a store (IKEA, PricesMart, etc.). """
    name = models.CharField(max_length=128)

    def __str__(self):
        """ String representation for model. """
        return self.name


class Order(models.Model):
    """ Representation of a store (IKEA, PricesMart, etc.). """
    date = models.DateField()
    store = models.ForeignKey(Store)

    def __str__(self):
        """ String representation for model. """
        return "{} - {}".format(self.store.name, self.date)
