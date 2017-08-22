import inspect
from jsonschema import validate
from collections import OrderedDict
from .converters import convert_to_html
from .widgets import parse_widget_form_data
from .dashboard import Dashboard
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

    def view(self, name, user_widgets=[], short=None):
        """
        name: the name that will appear in the UI
        user_widgets: list of Widget objects whose values
        will be given the user's functon
        short: a short name, for easy reference to this report later.
        Defaults to the actual name
        """
        if short is None:
            short = name
        def real_decorator(user_func):
            # save a ref to the user's func and widgets
            self.reports.append({
                'id': short,
                'name': name,
                'user_func': user_func,
                'widgets': user_widgets
            })
            # the func is not modified
            return user_func
        return real_decorator

    def compose_view(self, name, id_list, layout=None, short=None):
        """
        Creates a view that composes the specified views into a single view,
        arranged according to the given layout.

        id_list: list of IDs/short names of the reports to combine
        layout: a list of coordinate lists, in the same format as specified in
        the Dashboard constructor
        """
        # get all reports with matching names
        report_list = [report for report in self.reports if report['id'] in id_list]
        if len(report_list) < len(id_list):
            raise ValueError("one of the given reports was not found: {}".format(id_list))

        # concatenate the widgets of the reports
        all_widgets = []
        for r in report_list:
            all_widgets.extend(r['widgets'])

        # register a view that takes the list of all widgets, and gives the 
        # correct arguments to the correct reports
        @self.view(name, all_widgets, short)
        def view_func(*widget_args):
            # regenerate all reports, passing in the values from the relevant widgets
            remaining_args = widget_args
            results = []
            for r in report_list:
                num_widgets = len(r['widgets'])
                # pop this report's widget args from the list
                arg_list = remaining_args[:num_widgets]
                remaining_args = remaining_args[num_widgets:]
                # generate the figure
                output = r['user_func'](*arg_list)
                results.append(output)
            return Dashboard(results, layout)

    # func that generates the figure by passing the user func the 
    # parsed form data, then converting the func's output to HTML
    def generate_figure_html(self, report, form_data={}):
        inputs = parse_widget_form_data(report['widgets'], form_data)
        user_func = report['user_func']
        try:
            output = user_func(*inputs)
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
        for index, widget in enumerate(report['widgets']):
            # the widget type is the name of its python class
            # the JS setup func is Reports.Widgets.setupMap[widget_type]
            widget_type = type(widget).__name__
            html = widget.generateHTML(index)
            data = {'type': widget_type, 'html': html}
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
                        'type': 'array'
                    }
                },
                'required': ['reportIndex', 'widgetValues'],
            }
            validate(json, base_schema)
            report_index = json['reportIndex']
            report = self.reports[report_index]
            widgets = report['widgets']

            # validate all of the given widget values in 'widgetValues'
            inputs = json['widgetValues']
            if len(inputs) != len(widgets):
                raise ValueError("the widgetValues array has an incorrect number of items")
            for wid, value in zip(widgets, inputs):
                wid.validate_input(value)

        except Exception as e:
            raise ValidationError(str(e))

    def run(self, host=None, port=None, debug=None, **options):
        self.server.run(host, port, debug, **options)
