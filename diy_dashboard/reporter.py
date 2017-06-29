import inspect
import urllib
from collections import OrderedDict
from .converters import convert_to_html
from .widgets import parse_widget_form_data
from flask import Flask, render_template, request, abort

# make safe for URL path use
def normalize_report_name(name):
    name = name.replace(" ", "-")
    return urllib.parse.quote(name)        

def get_report_generators(figure_generator, widgets=[]):
    # transform widgets to tuple array, of (argName, widget)
    # this gives each widget a unique key b/c arg names must be unique
    argNames = inspect.getargspec(figure_generator)[0]
    for index, widget in enumerate(widgets):
        widgets[index] = (argNames[index], widget)
    print(widgets)

    def decorated_generator(widgetFormData={}):
        inputs = parse_widget_form_data(widgets, widgetFormData)
        output = figure_generator(**inputs)
        return convert_to_html(output)

    # NB: widgets must also be generated b/c jinja render_templates
    # requires an app context to run
    def widgets_generator():
        widgetsHTML = []
        for keyVal in widgets:
            name = keyVal[0]
            widget = keyVal[1]
            widgetsHTML.append(widget.generateHTML(name))
        return widgetsHTML

    return  {'figure_generator': decorated_generator,
            'widgets_generator': widgets_generator}

class Reporter:
    def __init__(self):
        self.report_generators = OrderedDict()
    
    def display(self, name, widgets=[]):
        url_name = normalize_report_name(name)
        def real_decorator(func):
            generators = get_report_generators(func, widgets)
            self.report_generators[url_name] = {'name': name, 'generators': generators}
            return func
        return real_decorator
    
    def get_reports(self):
        reports = []
        for key, value in self.report_generators.items():
            reports.append({'name': value['name'], 'href': key})
        return reports
    
    def html_for_report(self, reportname=None):
        # TODO: if no reportname specified, select the first report
        # (provided there are actually reports)
        if reportname is None:
            return render_template(
                    'index.html',
                    reports=self.get_reports())
        figure_report = self.report_generators.get(reportname, None)
        if figure_report is None:
            # TODO: either return index page or unknown report name page
            # probably unknown report name
            raise ValueError("invalid report name")
        figure_html = figure_report['generators']['figure_generator']()
        widgets_html = figure_report['generators']['widgets_generator']()
        return render_template(
                'figure_report.html',
                selectedReport=reportname,
                reports=self.get_reports(),
                figureHTML=figure_html,
                widgetsHTML=widgets_html)
        
    def html_for_figure(self, reportname, widget_values):
        figure_report = self.report_generators.get(reportname, None)
        if figure_report is None:
            # TODO: is this correct handling?
            raise ValueError("invalid report name")
        figure_generator = figure_report['generators']['figure_generator']
        reportHTML = figure_generator(widget_values)
        return reportHTML

    def run(self, host=None, port=None, debug=None, **options):
        app = Flask(__name__)

        @app.route('/')
        @app.route('/<reportname>')
        def index(reportname=None):
            return self.html_for_report(reportname)

        @app.route('/<reportname>', methods=['POST'])
        def updateFigure(reportname):
            print(request.get_json())
            return self.html_for_figure(reportname, request.get_json())

        app.run(host, port, debug, **options)
