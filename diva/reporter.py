import inspect
from jsonschema import validate
from collections import OrderedDict
from .converters import convert_to_html
from .widgets import parse_widget_form_data
from .exceptions import *
from flask import Flask, render_template, request, abort

class Diva():
    def __init__(self):
        """
        Sample doc string for testing autodocs
        """
        self.reports = []
        self.setup_server()

    def setup_server(self):
        """
        Sets up an internal Flask server
        """
        self.server = Flask(__name__)

        @self.server.route('/')
        def index():
            return self.get_index()

        @self.server.route('/update', methods=['POST'])
        def update_figure():
            body = request.get_json()
            self.validate_request(body)
            report_index = body['reportIndex']
            report = self.reports[report_index]
            return self.generate_figure_html(report, body['widgetValues'])

    def __call__(self, environ, start_response):
        """
        This allows a Diva object to act as a wsgi entry point.
        Just delegates the wsgi callable to the underlying flask server
        """
        return self.server.wsgi_app(environ, start_response)

    def view(self, name, user_widgets=[]):
        """
        testing
        """
        def real_decorator(user_func):
            # widgets is an array of (argName, widget)
            # this gives each widget a unique key b/c arg names must be unique
            # note that if the widget list is invalid for the given argspec, an
            # exception will be raised and caught in generate_figure_html
            arg_names = inspect.getargspec(user_func).args
            if len(arg_names) < len(user_widgets):
                error_message = """
                Your function {} takes {} positional arguments, but you specified {} widgets.
                If your function uses *varargs or **kwargs, please see the Diva docs for what to do.
                """.format(user_func.__name__, len(arg_names), len(user_widgets))
                raise WidgetsError(error_message) 
            # note that this is truncated to the len of the arg_names list, since
            # arg_names must be the shorter list
            widgets = list(zip(arg_names, user_widgets))

            # save a ref to the user's func and widgets
            self.reports.append({
                'name': name,
                'user_func': user_func,
                'widgets': widgets
            })

            # the func is not modified
            return user_func
        return real_decorator

    # func that generates the figure by passing the user func the 
    # parsed form data, then converting the func's output to HTML
    def generate_figure_html(self, report, widgetFormData={}):
        inputs = parse_widget_form_data(report['widgets'], widgetFormData)
        user_func = report['user_func']
        try:
            output = user_func(**inputs)
        except TypeError as err:
            error_message = """
            A TypeError was raised when Diva called your function like: {}(**kwargs), where kwargs = {}.
            Please double-check that you have a valid number of widgets,
            and see the Diva docs for help.
            """.format(user_func.__name__, inputs)
            raise WidgetsError(error_message)
        return convert_to_html(output)

    # NB: widgets must also be generated b/c jinja render_templates
    # requires an app context to run
    def generate_widget_data(self, report):
        widget_data = []
        for name, widget in report['widgets']:
            # the widget type is the name of its python class
            # the JS setup func is Reports.Widgets.setupMap[widget_type]
            widget_type = type(widget).__name__
            html = widget.generateHTML(name)
            data = {'name': name, 'type': widget_type, 'html': html}
            widget_data.append(data)
        return widget_data
            
    def get_index(self):
        report_data = []
        for report in self.reports:
            widgets = self.generate_widget_data(report)
            report_data.append({'name': report['name'], 'widgets': widgets})
        return render_template(
                'index.html',
                reports=report_data)
            
    def validate_request(self, json):
        try:
            base_schema = {
                'type': 'object',
                'properties': {
                    'reportIndex': {
                        'type': 'integer',
                        'minimum': 0,
                        'maximum': len(self.reports) - 1
                    },
                    # validated differently by report
                    'widgetValues': {
                        'type': 'object'
                    }
                },
                'required': ['reportIndex', 'widgetValues'],
            }
            validate(json, base_schema)
            report_index = json['reportIndex']

            # validate all of the given widget values in 'widgetValues'
            inputs = json['widgetValues']
            report = self.reports[report_index]
            for name, widget in report['widgets']:
                value = inputs.get(name, None)
                if value is None:
                    raise ValueError('widgetValues contains no value for the widget {}'.format(name))
                else:
                    widget.validate_input(value)    
        except Exception as e:
            raise ValidationError(e.message)

    def run(self, host=None, port=None, debug=None, **options):
        self.server.run(host, port, debug, **options)
