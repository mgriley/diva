import inspect
import urllib
from jsonschema import validate
from collections import OrderedDict
from .converters import convert_to_html
from .widgets import parse_widget_form_data
from flask import Flask, render_template, request, abort

class Reporter:
    def __init__(self):
        self.reports = []
    
    def display(self, name, *user_widgets):
        def real_decorator(user_func):
            # TODO: clean up this part, could encounter an error here
            # transform widgets to tuple array, of (argName, widget)
            # this gives each widget a unique key b/c arg names must be unique
            widgets = list(user_widgets)
            argNames = inspect.getargspec(user_func)[0]
            for index, widget in enumerate(widgets):
                widgets[index] = (argNames[index], widget)

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
        for report in self.reports:
            widgets = self.generate_widget_data(report)
            report_data.append({'name': report['name'], 'widgets': widgets})
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
            report = self.reports[report_index]
            return self.generate_figure_html(report, body['widgetValues'])

        app.run(host, port, debug, **options)
