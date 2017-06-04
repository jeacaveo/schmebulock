""" Module for general purpose functions. """


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
