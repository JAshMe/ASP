"""
This module will consist of all the Utility Form Functions
"""


def update_attr(field, attr, value):
    """
    To update the attribute of passed form field
    :param field: FormField Object
    :param attr: String: Attribute to change
    :param value: String: Value of attribute
    """

    field.widget.attrs.update({
        attr: value
    })


def update_all_inputs(field_dict, attr, value):
    """
    To update all the inputs of a form
    :param field_dict: Dic containing all the FormFields
     :param attr: String: Attribute to change
    :param value: String: Value of attribute
    """

    for field in field_dict:
        field_dict[field].widget.attrs.update({
            attr: value
        })
