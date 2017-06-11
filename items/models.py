""" Models for items app. """
from django.db import models

from audit_log.models import AuthStampedModel
from django_extensions.db.models import TimeStampedModel
from django_measurement.models import MeasurementField
from djmoney.models.fields import MoneyField
from measurement.measures import Volume, Weight


class Brand(AuthStampedModel, TimeStampedModel, models.Model):
    """ Representation of a brand (IKEA, Pampers, etc.). """
    name = models.CharField(max_length=128)

    def __str__(self):
        """ String representation for model. """
        return self.name


class Store(AuthStampedModel, TimeStampedModel, models.Model):
    """ Representation of a store (IKEA, PricesMart, etc.). """
    name = models.CharField(max_length=128)

    def __str__(self):
        """ String representation for model. """
        return self.name


class Order(AuthStampedModel, TimeStampedModel, models.Model):
    """ Representation of a store (IKEA, PricesMart, etc.). """
    date = models.DateField()
    store = models.ForeignKey(Store)

    def __str__(self):
        """ String representation for model. """
        return "{0} - {1}".format(self.store.name, self.date)


class Item(AuthStampedModel, TimeStampedModel, models.Model):
    """
    Representation of an item:
        Blue Cheese (Generic), 0.5 kg
        Bacon (XXX), 1.0 lb

    """
    name = models.CharField(max_length=128)
    volume = MeasurementField(measurement=Volume, null=True, blank=True,
                              help_text="Unit in DB is always cubic meters")
    weight = MeasurementField(measurement=Weight, null=True, blank=True,
                              help_text="Unit in DB is always grams")
    brand = models.ForeignKey(Brand)

    def __str__(self):
        """ String representation for model. """
        return "{0} ({1}), {2}".format(
            self.name, self.brand.name, self.volume or self.weight)


class Purchase(AuthStampedModel, TimeStampedModel, models.Model):
    """
    Representation of the purchase of an item (with an order if available):
        Blue Cheese (Generic), 0.5 kg at 50.00 DOP - #1
        Bacon (XXX), 1.0 lb at 1.00 USD - #N/A

    """
    price = MoneyField(max_digits=15, decimal_places=3, default_currency="USD")
    item = models.ForeignKey(Item)
    order = models.ForeignKey(Order, null=True, blank=True)

    def __str__(self):
        """ String representation for model. """
        return "{0} at {1} - #{2}".format(
            self.item, self.price, self.order.id if self.order else "N/A")
