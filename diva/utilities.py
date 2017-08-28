from flask import render_template
from .widgets import parse_widget_form_data, validate_widget_form_data, widgets_template_data
from functools import singledispatch
from flask import send_file, jsonify
import base64

def file_response(name, filepath):
    """
    name: when the client downloads the file, it will be called this (ex. "my_file.csv")

    filepath: path to the file that should be sent to the client
    """
    with open(filepath, 'rb') as content_file:
        file_bytes = content_file.read()
        encoded_bytes = base64.b64encode(file_bytes)
        response = {
            'filename': name,
            'content': encoded_bytes.decode('utf-8')
        }
        return jsonify(response)

# map from type to list of utils for that type
type_utils = {}

def label_utility(ui_name):
    """
    Get a label utility with the given name
    """
    def gen_html(val):
        return render_template('utility_label.html', name=ui_name)
    # this will never be called
    def apply(val, form_data):
        pass
    return {'generate_html': gen_html, 'apply': apply}

def register_simple_util(ui_name, some_type, widgets=[]):
    """
    Helper function for register_widget_util.

    widgets: a list of widgets. The values of these widgets are passed to
    the decorated function like ``your_func(val, *widget_values)``

    This is meant to decorate a function that takes the view value as its first
    argument, followed by a list of arguments that are given by widgets. It returns 
    the result of a call to ``file_response``
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
    ui_name: the name of this utility in the UI

    some_type: this utility will appear in the sidebar whenever your view function
    returns a value of type ``some_type``

    gen_widgets(val): a function that takes the report value (of the specified type), and 
    returns a list of widgets. These widget values will be passed like:
    ``apply_with_params(val, *widget_values)``.

    apply_with_params: a function that takes the report value (of the specified type) as 
    its first parameter, followed by a list of arguments that are given by widgets. The function must
    return the result of a call to ``file_response``
    """
    def gen_html(val):
        widgets = gen_widgets(val)
        widget_data = widgets_template_data(widgets)
        return render_template('utility_button.html', name=ui_name, widgets=widget_data)

    def apply_util(val, data):
        widgets = gen_widgets(val)
        validate_widget_form_data(widgets, data)
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
