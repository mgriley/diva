from flask import render_template

# map from type to list of utils for that type
type_utils = {}

def register_util(ui_name, some_type, widgets=[]):
    """
    meant to be used with decorator syntax
    A helper around general-purpose util registration. This should
    be sufficient for most utils
    """
    def decorator(user_func):
        """
        user_func must take a val, followed by widget-given arguments
        """
        def generate_html(val):
            """
            TODO: Generate an HTML form complete with widgets to meet the user's needs
            To get the div via jquery in the inline script: look for sibling with the same
            The script doesn't need to be sent with every util (b/c it doesn't change), but it
            must be executed with every one. Double-check how this works, may do this automatically
            via the cache.
            """
            return render_template('utility_button.html', 'name': ui_name)

        def get_response(val, data):
            # TODO: verify that this exists
            widget_values = data.get('widgetValues', [])
            # TODO: parse the widget data like normal
            return user_func(val, *data)

        register_util_for_type(some_type, generate_html, get_response)
        return user_func

    return decorator

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

def get_utils_for_type(some_type):
    return type_utils.get(some_type, [])    

def get_utilities_for_value(val):
    utils = get_utils_for_type(type(val))
    return utils
