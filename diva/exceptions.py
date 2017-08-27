class ValidationError(Exception):
    pass

class WidgetsError(Exception):
    pass

class WidgetInputError(Exception):
    def __init__(self, user_func, inputs):
        self.message = """
        A TypeError was raised when Diva called your function like: {}(**kwargs), where kwargs = {}.
        Please double-check that you have a valid number of widgets,
        and see the Diva docs for help.
        """.format(user_func.__name__, inputs)
