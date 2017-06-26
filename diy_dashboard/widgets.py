from flask import render_template
import time
from datetime import date, datetime, timedelta
from dateutil.relativedelta import *

class Widget:
    def parseForm(self, formData):
        return formData

    def default_value(self):
        return self.default

class InputTagWidget(Widget):
    def generateHTML(self, widgetId):
        return render_template('input_tag_widget.html',
                description=self.description,
                name=widgetId, attributes=self.attributes)

class TextWidget(InputTagWidget):
    def __init__(self, description, default="", placeholder=None):
        self.description = description
        self.default = default
        self.attributes = {'type': 'text', 'value': default,
                'placeholder': placeholder}

class FloatWidget(InputTagWidget):
    def __init__(self, description, default=0, minVal=None, maxVal=None,
            step=0.001):
        self.description = description
        self.default = default
        self.attributes = {'type': 'number', 'value': default,
                'min': minVal, 'max': maxVal, 'step': step}

    def parseForm(self, formData):
        try:
            return float(formData)
        except ValueError:
            return self.default

class IntWidget(FloatWidget):
    def __init__(self, description, default=0, minVal=None, maxVal=None):
        super(IntWidget, self).__init__(description, default, minVal, maxVal, step=1)

    def parseForm(self, formData):
        try:
            return int(formData)
        except ValueError:
            return self.default

class CheckBox(Widget):
    def __init__(self, description, default=False):
        self.description = description
        self.default = default
        self.attributes = {'type': 'checkbox'}
        
    def generateHTML(self, widgetId):
        return render_template('checkbox_widget.html',
                description=self.description,
                name=widgetId, attributes=self.attributes,
                checked=self.default)

    def parseForm(self, formData):
        try:
            return bool(formData)
        except ValueError:
            return self.default

class SelectOne(Widget):
    # default is index into the choices array
    def __init__(self, choices, default=None):
        self.choices = choices
        if default is None:
            self.default = choices[0]
        else:
            self.default = default

    def generateHTML(self, widgetId):
        return render_template('radio_widget.html',
                name=widgetId, choices=self.choices,
                defaultChoice=self.default)

class SelectAny(Widget):
    def __init__(self, choices, default=[]):
        self.choices = choices
        self.default = default

    def generateHTML(self, widgetId):
        return render_template('checklist_widget.html',
                name=widgetId, choices=self.choices,
                default=self.default)

# TODO: input and output are both in hexidecimal. user should be 
# responsible for the conversion
class Color(InputTagWidget):
    def __init__(self, description, default='#000000'):
        self.description=description
        self.default = default
        self.attributes = {'type': 'color', 'value': default}

class Date(InputTagWidget):
    # defaults to current date
    def __init__(self, description, default=None, minDate=None, maxDate=None):
        self.description = description
        if default is not None:
            self.default = default
        else:
            self.default = time.strftime('%Y-%m-%d')
        
        self.attributes = {'type': 'date', 'value': self.default,
                'min': minDate, 'max': maxDate}

class Month(Date):
    def __init__(self, description, default=None):
        self.description = description
        if default is not None:
            self.default = default
        else:
            self.default = time.strftime('%Y-%m')

        self.attributes = {'type': 'month', 'value': self.default}

class Week(Date):
    def __init__(self, description, default=None):
        self.description = description
        self.default = default if default is not None else time.strftime('%Y-W%W')
        self.attributes = {'type': 'week', 'value': self.default}

# NB: times are in 24hr format
class Time(Date):
    def __init__(self, description, default=None):
        self.description = description
        self.default = default if default is not None else time.strftime('%H:%M')
        self.attributes = {'type': 'time', 'value': self.default}

class Slider(Widget):
    def __init__(self, description, default=1, valRange=(0, 1), numDecimals=4):
        self.description = description
        self.valRange = valRange
        self.default = default
        self.numDecimals = numDecimals
        step = 1 / (10 ** numDecimals);
        self.attributes = {'type': 'range', 'min': self.valRange[0],
                'max': self.valRange[1], 'step': step, 'value': self.default}

    def generateHTML(self, widgetId):
        return render_template('slider_widget.html',
                name=widgetId,
                description=self.description,
                default=('{:.{}f}').format(self.default, self.numDecimals),
                attributes=self.attributes)

    def parseForm(self, formData):
        return FloatWidget.parseForm(self, formData)

# classes and helpers for internally working with date ranges

def iso_to_date(isoStr):
    dt = datetime.strptime(isoStr, '%Y-%m-%d')
    return dt.date()

class DateRangeModel():
    # start and end are date objects
    def start_date(self):
        pass
    
    def end_date(self):
        pass

    def iso_start(self):
        return self.start_date().isoformat()

    def iso_end(self):
        return self.end_date().isoformat()
        
class AbsoluteDateRange(DateRangeModel):
    def __init__(self, start, end):
        self.start = start
        self.end = end 
    def start_date(self):
        return self.start
    def end_date(self):
        return self.end

class HalfAbsoluteDataRange(AbsoluteDateRange):
    def __init__(self, start):
        self.start = start
    def end_date(self):
        return date.today()

class RelativeDateRange(DateRangeModel):
    # offsets are time-deltas wrt present
    def __init__(self, start_offset, end_offset):
        self.start_offset = start_offset
        self.end_offset = end_offset
    def start_date(self):
        return date.today() - self.start_offset
    def end_date(self):
        return date.today() - self.end_offset

# helpers for specifying date ranges

def abs_range(startStr, endStr):
    start = iso_to_date(startStr)
    end = iso_to_date(endStr)
    return AbsoluteDateRange(start, end)

def last(days=0, weeks=0, months=0, years=0):
    start_offset = relativedelta(days=days, weeks=weeks, months=months, years=years)
    end_offset = timedelta()
    return RelativeDateRange(start_offset, end_offset)

def rel_range(durA, durB=timedelta()):
    return RelativeDateRange(durA, durB)

def date_to_present(start_str):
    start_date = iso_to_date(start_str)
    return HalfAbsoluteDataRange(start_date)    

class DateRange(Widget):

    def __init__(self, description, default=last(weeks=1)):
        self.description = description
        self.default = default
        date = '{} to {}'.format(self.default.iso_start(),
                self.default.iso_end())
        print(date)
        self.attributes = {'type': 'text',
                'value': date,
                'size': len(date),
                'data-startdate': self.default.iso_start(),
                'data-enddate': self.default.iso_end()}

    def generateHTML(self, widgetId):
        return render_template('daterange_widget.html',
                name=widgetId,
                description=self.description,
                attributes=self.attributes)
    
    def default_value(self):
        return (self.default.start_date(), self.default.end_date())
    
    # TODO: use schema to verify that formData is 2-elem array
    def parseForm(self, formData):
        formData = formData.split(' to ')
        start = iso_to_date(formData[0])
        end = iso_to_date(formData[1])
        return (start, end)

# given map of form data, return a map of inputs 
def parse_widget_form_data(widgets, widgetFormData):
    inputs = {}
    for keyVal in widgets:
        name = keyVal[0]
        widget = keyVal[1]
        formData = widgetFormData.get(name, None)
        if formData == None:
            inputs[name] = widget.default_value();
        else:
            inputs[name] = widget.parseForm(formData)
    return inputs
