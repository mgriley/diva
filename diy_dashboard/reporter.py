import inspect
from flask import render_template
from diy_dashboard.converters import convert_to_html
from diy_dashboard.widgets import parse_widget_form_data

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
        self.report_generators = {}
    
    def display(self, name, widgets=[]):
        def real_decorator(func):
            generators = get_report_generators(func, widgets)
            self.report_generators[name] = generators
            return func
        return real_decorator
    
    def get_reports(self):
        reports = []
        for key, value in self.report_generators.items():
            reports.append({'name': key, 'href': key})
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
        figure_html = figure_report['figure_generator']()
        widgets_html = figure_report['widgets_generator']()
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
        figure_generator = figure_report['figure_generator']
        reportHTML = figure_generator(widget_values)
        return reportHTML
