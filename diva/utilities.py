from flask import render_template
from .widgets import parse_widget_form_data
from functools import singledispatch

# map from type to list of utils for that type
type_utils = {}

def register_simple_util(ui_name, some_type, widgets=[]):
    """
    Helper for register_widget_util
    meant to be used with decorator syntax
    A helper for utils where the user input options do not depend on the 
    current value. That is, the options are the same for every value of the
    given type.
    """
    def decorator(user_func):
        """
        user_func must be like appy_func followed by widget-set args
        """
        register_widget_util(ui_name, some_type, lambda val: widgets, user_func)
        return user_func

    return decorator

def register_widget_util(ui_name, some_type, gen_widgets, apply_with_params):
    """
    Helper for register_util_for_type
    A helper for creating utilities, using the existing widgets system for params

    gen_widgets: func that takes a figure value and returns a list of widgets for the util

    apply_util: func that takes a figure value followed by a list of args that the widget values will
    be passed to
    """
    def gen_html(val):
        widgets = gen_widgets(val)
        # TODO: generate the widget HTML
        return render_template('utility_button.html', name=ui_name)

    def apply_util(val, data):
        widgets = gen_widgets(val)
        inputs = parse_widget_form_data(widgets, data)
        return apply_with_params(val, *inputs)

    register_util_for_type(some_type, gen_html, apply_util)

def register_util_for_type(my_type, gen_html, apply_util):
    """
    gen_html: func that takes a value and returns the html for the utility
    that works with that value

    apply_util: func that takes a value and form_data dict. returns whatever the
    flask server should return to the browser
    """
    if my_type not in type_utils:
        type_utils[my_type] = []
    util = {'generate_html': gen_html, 'apply': apply_util}
    type_utils[my_type].append(util)

@singledispatch
def get_utilities_for_value(val):
    return type_utils.get(type(val), [])    
