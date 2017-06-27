from flask import render_template
import time
from datetime import date, time, datetime, timedelta
from dateutil.relativedelta import *
from functools import singledispatch

class Input():
    def generateHTML(self, widgetId):
        return ''

    def parseForm(self, formData):
        pass

    def default_value(self):
        return self.default

class Widget(Input):
    def parseForm(self, formData):
        return formData

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

class DateModel():
    def value(self):
        pass
    def iso(self):
        return self.value().isoformat()

class AbsoluteDate(DateModel):
    def __init__(self, date):
        self.date = date

    def value(self):
        return self.date

class RelativeDate(DateModel):
    def __init__(self, duration):
        self.duration = duration

    def value(self):
        return date.today() - self.duration

# convert the specified date to a date model
@singledispatch
def to_date_model(date):
    raise ValueError("given date must be: a) ISO format string, b) datetime.date object, c) datetime.timedelta object, or d) dateutil.relativedelta object")

@to_date_model.register(date)
def date_to_model(date):
    return AbsoluteDate(date)

@to_date_model.register(str)
def iso_to_model(date_str):
    return AbsoluteDate(iso_to_date(date_str))

@to_date_model.register(timedelta)
@to_date_model.register(relativedelta)
def delta_to_model(date_delta):
    return RelativeDate(date_delta)

class DateRange(Widget):

    def __init__(self, description, start=relativedelta(), end=relativedelta()):
        self.description = description
        self.start_date = to_date_model(start)
        self.end_date = to_date_model(end)
        date = '{} to {}'.format(self.start_date.iso(),
                self.end_date.iso())
        print(date)
        self.attributes = {'type': 'text',
                'value': date,
                'size': len(date),
                'data-startdate': self.start_date.iso(),
                'data-enddate': self.end_date.iso()}

    def generateHTML(self, widgetId):
        return render_template('daterange_widget.html',
                name=widgetId,
                description=self.description,
                attributes=self.attributes)
    
    def default_value(self):
        return (self.start_date.value(), self.end_date.value())
    
    # TODO: use schema to verify that formData is 2-elem array
    def parseForm(self, formData):
        formData = formData.split(' to ')
        start = iso_to_date(formData[0])
        end = iso_to_date(formData[1])
        return (start, end)

class Date(InputTagWidget):
    def __init__(self, description, default=relativedelta()):
        self.description = description
        self.default = to_date_model(default)
        self.attributes = {'type': 'date', 'value': self.default.iso()}

    def default_value(self):
        return self.default.value()

    def parseForm(self, formData):
        return iso_to_date(formData)

# NB: times are in 24hr format
class Time(InputTagWidget):
    def __init__(self, description, default=time()):
        self.description = description
        self.default = default
        time_str = self.default.strftime('%H:%M')
        self.attributes = {'type': 'time', 'value': time_str}

    def parseForm(self, formData):
        print(formData)
        dt = datetime.strptime(formData, '%H:%M')
        print(dt)
        return dt.time()


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
