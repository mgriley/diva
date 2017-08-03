import inspect
import urllib
from jsonschema import validate
from collections import OrderedDict
from .converters import convert_to_html
from .widgets import parse_widget_form_data
from flask import Flask, render_template, request, abort

def get_report_generators(user_func, widgets=[]):
    # transform widgets to tuple array, of (argName, widget)
    # this gives each widget a unique key b/c arg names must be unique
    argNames = inspect.getargspec(user_func)[0]
    for index, widget in enumerate(widgets):
        widgets[index] = (argNames[index], widget)

    # func that generates the figure by passing the user func the 
    # parsed form data, then converting the func's output to HTML
    def figure_generator(widgetFormData={}):
        inputs = parse_widget_form_data(widgets, widgetFormData)
        output = user_func(**inputs)
        return convert_to_html(output)

    # NB: widgets must also be generated b/c jinja render_templates
    # requires an app context to run
    def widgets_generator():
        widget_data = []
        for name, widget in widgets:
            # the widget type is the name of its python class
            # the JS setup func is Reports.Widgets.setupMap[widget_type]
            widget_type = type(widget).__name__
            # TODO: may not need to pass in name like this anymore
            html = widget.generateHTML(name)
            data = {'name': name, 'type': widget_type, 'html': html}
            widget_data.append(data)
        return widget_data

    # also TODO: there is no need for this crazy amount of closure,
    # why not just keep references to the figure and widgets, then
    # call these functions in the reporter class, thereby 
    # simplifying everything...
    # TODO: left off here. Figure out how to do validation.
    # Do the validation in parseForm, that is the easiest!
    # generate a json schema for the request object required to
    # update this report
    # def widgets_validator():
            
    # widget_names = [w[0] for w in widgets]
    # properties = {}
    # for name, widget in widgets:
        # properties[name] = {}
    # widgets_schema = {
        # 'properties': properties
        # 'required': widget_names,
        # 'additionalProperties': False
    # }

    return  {'figure_generator': figure_generator,
            'widgets_generator': widgets_generator}

class Reporter:
    def __init__(self):
        self.report_generators = OrderedDict()
    
    def display(self, name, widgets=[]):
        def real_decorator(func):
            # create the functions that generate a report for the 
            # given func
            generators = get_report_generators(func, widgets)
            self.report_generators[name] = generators
            # the func is not modified
            return func
        return real_decorator
    
    def get_reports(self):
        reports = []
        for key, value in self.report_generators.items():
            widgets = value['widgets_generator']()
            reports.append({'name': key, 'widgets': widgets})
        return reports
    
    def get_index(self):
        return render_template(
                'index.html',
                reports=self.get_reports())
        
    def html_for_figure(self, report_name, widget_values):
        figure_report = self.report_generators.get(report_name, None)
        figure_generator = figure_report['figure_generator']
        reportHTML = figure_generator(widget_values)
        return reportHTML
    
    def validate_request(self, json, base_schema):
        validate(json, base_schema)
        report_index = json['reportIndex']
        # TODO
        # widgets_schema = self.report_generators['widgets_schema']
        # validate(json['widgetValues'], widgets_schema)

    def create_schema(self):
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
        return base_schema

    def run(self, host=None, port=None, debug=None, **options):
        schema = self.create_schema()

        # setup the server
        app = Flask(__name__)

        @app.route('/')
        def index():
            return self.get_index()

        @app.route('/update', methods=['POST'])
        def update_figure():
            print(request.get_json())
            body = request.get_json()
            self.validate_request(body, schema)
            report_index = body['reportIndex']
            dict_items = list(self.report_generators.items())
            report_name = dict_items[report_index][0]
            return self.html_for_figure(report_name, body['widgetValues'])

        app.run(host, port, debug, **options)
