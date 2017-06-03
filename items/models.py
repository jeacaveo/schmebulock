""" Models for items app. """
from django.db import models


class Brand(models.Model):
    """ Representation of a brand (IKEA, Pampers, etc.). """
    name = models.CharField(max_length=128)

    def __str__(self):
        """ String representation for model. """
        return self.name
