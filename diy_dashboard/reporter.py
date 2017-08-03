import inspect
import urllib
from jsonschema import validate
from collections import OrderedDict
from .converters import convert_to_html
from .widgets import parse_widget_form_data
from flask import Flask, render_template, request, abort

class Reporter:
    def __init__(self):
        self.reports = OrderedDict()
    
    def display(self, name, widgets=[]):
        def real_decorator(user_func):
            # transform widgets to tuple array, of (argName, widget)
            # this gives each widget a unique key b/c arg names must be unique
            argNames = inspect.getargspec(user_func)[0]
            for index, widget in enumerate(widgets):
                widgets[index] = (argNames[index], widget)

            

            # save a ref to the user's func and widgets
            self.reports[name] = {
                'user_func': user_func,
                'widgets': widgets
            }

            # the func is not modified
            return user_func
        return real_decorator

    # func that generates the figure by passing the user func the 
    # parsed form data, then converting the func's output to HTML
    def generate_figure_html(self, report, widgetFormData={}):
        inputs = parse_widget_form_data(report['widgets'], widgetFormData)
        output = report['user_func'](**inputs)
        return convert_to_html(output)

    # NB: widgets must also be generated b/c jinja render_templates
    # requires an app context to run
    def generate_widget_data(self, report):
        widget_data = []
        for name, widget in report['widgets']:
            # the widget type is the name of its python class
            # the JS setup func is Reports.Widgets.setupMap[widget_type]
            widget_type = type(widget).__name__
            # TODO: may not need to pass in name like this anymore
            html = widget.generateHTML(name)
            data = {'name': name, 'type': widget_type, 'html': html}
            widget_data.append(data)
        return widget_data
            
    def get_index(self):
        report_data = []
        for name, report in self.reports.items():
            widgets = self.generate_widget_data(report)
            report_data.append({'name': name, 'widgets': widgets})
        return render_template(
                'index.html',
                reports=report_data)
            
    def validate_request(self, json):
        base_schema = {
            'type': 'object',
            'properties': {
                'reportIndex': {
                    'type': 'integer',
                    'minimum': 0,
                    'maximum': len(self.report_generators) - 1
                },
                # validated differently by report
                'widgetValues': {
                    'type': 'object'
                }
            },
            'required': ['reportIndex', 'widgetValues'],
            'additionalProperties': False
        }
        validate(json, base_schema)
        report_index = json['reportIndex']

        # the widgetValues object must have a value for every widget
        widget_names = [w[0] for w in widgets]
        properties = {}
        for name, widget in widgets:
            properties[name] = {}
        widgets_schema = {
            'properties': properties
            'required': widget_names,
            'additionalProperties': False
        }

        # TODO: left off here. Don't any of the above code, just check
        # for existence here
        # verify the contents of the widgetValues object
        # loop through all widgets, called validate_input

    def run(self, host=None, port=None, debug=None, **options):

        # setup the server
        app = Flask(__name__)

        @app.route('/')
        def index():
            return self.get_index()

        @app.route('/update', methods=['POST'])
        def update_figure():
            print(request.get_json())
            body = request.get_json()
            self.validate_request(body)
            report_index = body['reportIndex']
            dict_items = list(self.reports.items())
            report_name = dict_items[report_index][0]
            report = self.reports.get(report_name, None)
            return self.generate_figure_html(report, body['widgetValues'])

        app.run(host, port, debug, **options)
