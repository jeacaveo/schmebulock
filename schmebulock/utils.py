""" Module for general purpose functions. """
from collections import OrderedDict


def get_model_fields(model):
    """
    Get fields list for a model.

    (To avoid direct call to _meta attribute and linting warnings)

    Parameters:
        model: django.db.models.Model

    Returns:
        list

    """
    return [field.name for field in getattr(model, '_meta').fields]


def get_choices(data, first=None):
    """
    Turns a dict into a list of tuples with two values:
       First item as the value.
       Second item as the key.

    If 'first' parameter is provided for a valid key in 'data', that item will
    be the first one in the resulting list.

    (This is the inverse behavior from dict.items())

    Parameters:
        data: dict
            Dict to transform.
        first: str
            Key to use as first value.

    Returns:
        list(tuple)

    """
    data = OrderedDict(data.items())

    if first in data.keys():
        data.move_to_end(first, last=False)

    return [(val, key) for key, val in data.items()]
