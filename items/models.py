""" Models for items app. """
from django.db import models

from django_measurement.models import MeasurementField
from djmoney.models.fields import MoneyField
from measurement.measures import Volume, Weight


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
        return "{0} - {1}".format(self.store.name, self.date)


class Item(models.Model):
    """
    Representation of an item:
        Blue Cheese (Generic), 0.5 kg at 50.00 DOP
        Bacon (XXX), 1.0 lb at 1.00 USD

    """
    name = models.CharField(max_length=128)
    price = MoneyField(max_digits=15, decimal_places=3, default_currency='USD')
    volume = MeasurementField(measurement=Volume, null=True, blank=True,
                              help_text="Unit in DB is always cubic meters")
    weight = MeasurementField(measurement=Weight, null=True, blank=True,
                              help_text="Unit in DB is always grams")
    brand = models.ForeignKey(Brand)
    order = models.ForeignKey(Order)

    def __str__(self):
        """ String representation for model. """
        return "{0} ({1}), {2} at {3}".format(
            self.name,
            self.brand.name,
            self.volume or self.weight,
            self.price)
