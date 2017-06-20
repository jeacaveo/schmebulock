""" Custom metadata for items app. """
from rest_framework.metadata import SimpleMetadata

from measurement.measures import Volume, Weight

from schmebulock.utils import get_choices


class CustomItemMetadata(SimpleMetadata):
    """ Custom metadata class for Items endpoint. """

    # Override
    def get_field_info(self, field):
        """ Overriding to add custom unit_choices to required fields. """
        field_info = super().get_field_info(field)

        # Adding unit_choices to fields that need it.
        if field.field_name == "volume":
            field_info["unit_choices"] = get_choices(
                Volume.get_aliases(), first="cubic meter")
        elif field.field_name == "weight":
            field_info["unit_choices"] = get_choices(
                Weight.get_aliases(), first="gram")

        return field_info
