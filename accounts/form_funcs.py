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


def update_all_inputs(field_dict, attr, value, non_control_field=None):
    """
    To update all the inputs of a form
    :param field_dict: Dic containing all the FormFields
     :param attr: String: Attribute to change
    :param value: String: Value of attribute
    :param non_control_field: Dict containing non control fields
    """

    for field in field_dict:
        if (non_control_field is None) or (field not in non_control_field):
            field_dict[field].widget.attrs.update({
                attr: value
            })
