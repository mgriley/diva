import inspect
from jsonschema import validate
from collections import OrderedDict
from .converters import convert_to_html
from .widgets import (widgets_template_data, validate_widget_form_data,
        parse_widget_form_data, Skip, should_skip)
from .utilities import get_utilities_for_value
from .dashboard import Dashboard
from .exceptions import *
from flask import Flask, render_template, request, abort, jsonify

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
            report = self.get_report_from_body(body)
            self.validate_widget_values(report, body)
            response_data = self.update_report(report, body['widgetValues'])
            return jsonify(response_data)

        @self.server.route('/utility', methods=['POST'])
        def apply_utility():
            body = request.get_json()
            report = self.get_report_from_body(body)
            self.validate_utility_data(report, body)
            # get the utility
            utility_index = body['utilityIndex']
            utility = report['utilities'][utility_index]
            # apply the utility to the report's current value and 
            # any user-input sent with the post (for options)
            current_value = report['current_value']
            form_data = body['data']
            return utility['apply'](current_value, form_data)

    def __call__(self, environ, start_response):
        """
        This allows a Diva object to act as a wsgi entry point.
        Just delegates the wsgi callable to the underlying flask server
        """
        return self.server.wsgi_app(environ, start_response)

    def run(self, host=None, port=None, debug=None, **options):
        self.server.run(host, port, debug, **options)

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
        # also add labels between the widget groups
        all_widgets = []
        for index, r in enumerate(report_list):
            all_widgets.append(Skip('report {}'.format(index)))
            all_widgets.extend(r['widgets'])

        # register a view that takes the list of all widgets, and gives the 
        # correct arguments to the correct reports
        @self.view(name, all_widgets, short)
        def view_func(*widget_args):
            # regenerate all reports, passing in the values from the relevant widgets
            remaining_args = widget_args
            results = []
            for r in report_list:
                # get the number of widgets that pass their value to the underlying
                # function (that is, the number that shouldn't be skipped)
                active_widgets = [w for w in r['widgets'] if not should_skip(w)]
                num_widgets = len(active_widgets)
                # pop this report's widget args from the list
                # note that the Skip/label widgets are not passed to the view func
                # so there is no need to account for them 
                arg_list = remaining_args[:num_widgets]
                remaining_args = remaining_args[num_widgets:]
                # generate the figure
                output = r['user_func'](*arg_list)
                results.append(output)
            return Dashboard(results, layout)

    # func that generates the figure by passing the user func the 
    # parsed form data, then converting the func's output to HTML
    def update_report(self, report, form_data={}):
        inputs = parse_widget_form_data(report['widgets'], form_data)
        user_func = report['user_func']
        try:
            output = user_func(*inputs)
        except TypeError as err:
            raise WidgetInputError(user_func, inputs)
        utilities = get_utilities_for_value(output)
        # update the report
        report['current_value'] = output
        report['utilities'] = utilities
        # generate the HTML required to update the UI
        figure_html = convert_to_html(output)
        utilityHTML = [util['generate_html'](output) for util in utilities]
        response = {'figureHTML': figure_html, 'utilityHTML': utilityHTML}
        return response
                
    def get_index(self):
        report_data = []
        for report in self.reports:
            widgets = widgets_template_data(report['widgets'])
            report_data.append({'name': report['name'], 'widgets': widgets})
        return render_template(
                'index.html',
                reports=report_data)
            
    def validate_widget_values(self, report, json):
        inputs = json.get('widgetValues', [])
        validate_widget_form_data(report['widgets'], inputs)
        
    def validate_utility_data(self, report, json):
        try:
            schema = {
                'type': 'object',
                'properties': {
                    'utilityIndex': {
                        'type': 'integer',
                        'minimum': 0,
                        'maximum': len(report['utilities']) - 1
                    },
                    'data': {
                    }
                },
                'required': ['utilityIndex', 'data']
            }
            validate(json, schema)
        except Exception as e:
            raise ValidationError(str(e))

    def get_report_from_body(self, body):
        self.validate_request(body)
        report_index = body['reportIndex']
        return self.reports[report_index]

    def validate_request(self, json):
        try:
            schema = {
                'type': 'object',
                'properties': {
                    'reportIndex': {
                        'type': 'integer',
                        'minimum': 0,
                        'maximum': len(self.reports) - 1
                    }
                },
                'required': ['reportIndex'],
            }
            validate(json, schema)
        except Exception as e:
            raise ValidationError(str(e))
    
