""" Custom metadata for items app. """

from djmoney import settings as djmoney_settings
from measurement.measures import Volume, Weight
from rest_framework.metadata import SimpleMetadata

from schmebulock.utils import get_choices


class CustomItemMetadata(SimpleMetadata):
    """ Custom metadata class for Items endpoint. """

    # Override
    def get_field_info(self, field):
        """ Overriding to add custom unit_choices to required fields. """
        field_info = super().get_field_info(field)

        if field.field_name == "volume":
            field_info["unit_choices"] = get_choices(
                Volume.get_aliases(), first="cubic meter")
        elif field.field_name == "weight":
            field_info["unit_choices"] = get_choices(
                Weight.get_aliases(), first="gram")

        return field_info


class CustomPurchaseMetadata(SimpleMetadata):
    """ Custom metadata class for Purchases endpoint. """

    # Override
    def get_field_info(self, field):
        """ Overriding to add custom choices to currency field. """
        field_info = super().get_field_info(field)

        if field.field_name == "currency":
            field_info["choices"] = djmoney_settings.CURRENCY_CHOICES

        return field_info
