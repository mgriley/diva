from flask import render_template
from datetime import date, time, datetime, timedelta
from dateutil.relativedelta import *
from functools import singledispatch
from jsonschema import validate

class Widget():
    def generateHTML(self, widgetId):
        return ''

    def parseForm(self, formData):
        return formData

    def default_value(self):
        return self.default

class InputTagWidget(Widget):
    def generateHTML(self, widgetId):
        return render_template('input_tag_widget.html',
                description=self.description,
                name=widgetId, attributes=self.attributes)

class String(InputTagWidget):
    """
    Output: str
    """
    def __init__(self, description, default=""):
        """
        description(str): the text for this widget's label.
        """
        self.description = description
        self.default = default
        self.attributes = {'type': 'text', 'value': default}

    def validate_input(self, formData):
        schema = {'type': 'string'}
        validate(formData, schema)

# a helper for validation of numberical types
def set_schema_bounds(schema, min_val, max_val):
    if min_val is not None:
        schema['minimum'] = min_val
    if max_val is not None:
        schema['maximum'] = max_val

def validate_bounds(num, min_val, max_val):
    below_min = min_val is not None and num < min_val
    above_max = max_val is not None and max_val < num
    if below_min or above_max:
        raise ValueError("num is outside bounds")

class Float(InputTagWidget):
    """
    Output: float
    """
    def __init__(self, description, default=0, minVal=None, maxVal=None,
            step=0.001):
        """
        step: the interval between allowable values
        """
        self.description = description
        self.default = default
        self.minVal = minVal
        self.maxVal = maxVal
        self.attributes = {'type': 'number', 'value': default,
                'min': minVal, 'max': maxVal, 'step': step}

    def validate_input(self, formData):
        num = float(formData)
        validate_bounds(num, self.minVal, self.maxVal)
        
    def parseForm(self, formData):
        return float(formData)

class Int(Float):
    """
    Output: int
    """
    def __init__(self, description, default=0, minVal=None, maxVal=None):
        super().__init__(description, default, minVal, maxVal, step=1)

    def validate_input(self, formData):
        num = int(formData)
        validate_bounds(num, self.minVal, self.maxVal)

    def parseForm(self, formData):
        return int(formData)

class Bool(Widget):
    """
    Output: bool
    """
    def __init__(self, description, default=False):
        self.description = description
        self.default = default
        self.attributes = {'type': 'checkbox'}
        
    def generateHTML(self, widgetId):
        return render_template('checkbox_widget.html',
                description=self.description,
                name=widgetId, attributes=self.attributes,
                checked=self.default)

    def validate_input(self, formData):
        schema = {'type': 'boolean'}
        validate(formData, schema)

    def parseForm(self, formData):
        return bool(formData)

class SelectOne(Widget):
    """
    Output: the str that the user selected
    """

    # default is index into the choices array
    def __init__(self, description, choices, default=None):
        """
        * choices: a list of strings.
        * default: a string in ``choices``. If not specified, 
            the default will be the first string in ``choices``.
        """
        self.description = description
        self.choices = choices
        if default is None:
            self.default = choices[0]
        else:
            self.default = default

    def generateHTML(self, widgetId):
        return render_template('radio_widget.html',
                name=widgetId,
                description=self.description,
                choices=self.choices,
                defaultChoice=self.default)

    def validate_input(self, formData):
        schema = {
            'type': 'string',
            'enum': self.choices
        }
        validate(formData, schema)

class SelectSubset(Widget):
    """
    Output: A list of all the strings that the user selection. 
    It may be empty.
    """
    def __init__(self, description, choices, default=[]):
        """
        * choices: a list of strings
        * default: a list of strings in ``choices`` that will be 
            selected by default.
        """
        self.description = description
        self.choices = choices
        self.default = default

    def generateHTML(self, widgetId):
        return render_template('checklist_widget.html',
                name=widgetId,
                description=self.description,
                choices=self.choices,
                default=self.default)

    def validate_input(self, formData):
        schema = {
            'type': 'array',
            'uniqueItems': True,
            'additionalItems': False,
            'items': {
                'type': 'string',
                'enum': self.choices
            }
        }
        validate(formData, schema)

# TODO: keep in hexadecimal for now
# can later use the more effective:
# return as RGB triple (r, g, b) with values in [0, 1]
class Color(InputTagWidget):
    """
    Output: a hexadecimal string in the format #RRGGBB
    """
    def __init__(self, description, default='#000000'):
        self.description=description
        self.default = default
        self.attributes = {'type': 'color', 'value': default}

    def validate_input(self, formData):
        schema = {
            'type': 'string',
            'pattern': '^#([A-Fa-f0-9]{6})$'
        }
        validate(formData, schema)

    # TODO: this is for rgb triple
    # def validate_input(self, formData):
        # schema = {
            # 'type': 'array',
            # 'items': {
                # 'type': 'number',
                # 'minimum': 0,
                # 'maximum': 1
            # },
            # 'minLength': 3,
            # 'maxLength': 3
        # }
        # validate(formData, schema)

class Slider(Widget):
    """
    Slider has the same function as Float, the only difference is the UI
    Output: float
    """
    def __init__(self, description, default=1, valRange=(0, 1), numDecimals=4):
        """
        * valRange: (min, max) where min and max are floats
        * numDecimals: the number of decimal places to display in the UI
        """
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

    def validate_input(self, formData):
        num = float(formData)
        min_val, max_val = self.valRange
        validate_bounds(num, min_val, max_val)

    def parseForm(self, formData):
        return Float.parseForm(self, formData)

# classes and helpers for internally working with date ranges

def iso_to_date(isoStr):
    dt = datetime.strptime(isoStr, '%Y-%m-%d')
    return dt.date()

# the date can either by specified as absolute or relative 
# to the current date

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

# date obj converts to absolute date
@to_date_model.register(date)
def date_to_model(date):
    return AbsoluteDate(date)

# string is assumed to be an absolute date in ISO format
@to_date_model.register(str)
def iso_to_model(date_str):
    return AbsoluteDate(iso_to_date(date_str))

# delta objects convert to dates relative to the current date
# A positive delta is an offset into the past, not the future
# ex. a delta of 1 day means yesterday, not tomorrow
@to_date_model.register(timedelta)
@to_date_model.register(relativedelta)
def delta_to_model(date_delta):
    return RelativeDate(date_delta)

class Date(InputTagWidget):
    """
    Output: datetime.date    
    """
    def __init__(self, description, default=relativedelta()):
        """
        default: may either be provided as a:

        * datetime.date object
        * string of a date in ISO format (YYYY-mm-dd)
        * datetime.timedelta object. The date will be current - delta
        * dateutil.relativedelta object. The date will be current - delta

        If not specified, it will be the current date.
        Note that dateutil is not in the Python standard library. It provides a simpler
        API to specify a duration in days, weeks, months, etc. You can install it with pip.
        """
        self.description = description
        self.default = to_date_model(default)
        # see Bootstrap date picker docs for options
        # https://bootstrap-datepicker.readthedocs.io/en/stable/#
        self.attributes = {
            'data-date-format': 'yyyy-mm-dd',
            'data-date-orientation': 'left bottom',
            'data-date-autoclose': 'true',
            'value': self.default.iso(),
        }

    def default_value(self):
        return self.default.value()
    
    def validate_input(self, formData):
        schema = {'type': 'string'}
        validate(formData, schema)
        # throws ValueError if incorrect format
        iso_to_date(formData)

    def parseForm(self, formData):
        return iso_to_date(formData)

class DateRange(InputTagWidget):
    """
    Output: (start_date, end_date) of type (datetime.date, datetime.date)
    """

    def __init__(self, description, start=relativedelta(), end=relativedelta()):
        """
        ``start`` and ``end`` follow the same rules as ``default`` for ``Date``
        """
        self.description = description
        self.start_date = to_date_model(start)
        self.end_date = to_date_model(end)
        date = '{} to {}'.format(self.start_date.iso(),
                self.end_date.iso())
        self.attributes = {'type': 'text',
                'value': date,
                'size': len(date),
                'data-startdate': self.start_date.iso(),
                'data-enddate': self.end_date.iso()}
    
    def default_value(self):
        return (self.start_date.value(), self.end_date.value())
    
    def validate_input(self, formData):
        schema = {
            'type': 'array',
            'minLength': 2,
            'maxLength': 2,
            'items': {
                'type': 'string',
            }
        }
        validate(formData, schema)
        # strptime throws a value error if does not match the format
        for dateStr in formData:
            iso_to_date(dateStr)

    def parseForm(self, formData):
        start = iso_to_date(formData[0])
        end = iso_to_date(formData[1])
        return (start, end)

# TODO: use the same lazy eval as done with datetime.date objects
# NB: times are in 24hr format
class Time(InputTagWidget):
    """
    Output: datetime.time object   
    """
    def __init__(self, description, default=time()):
        """
        default: datetime.time object
        """
        self.description = description
        self.default = default
        time_str = self.default.strftime('%H:%M')
        self.attributes = {
            'value': time_str
        }

    def validate_input(self, formData):
        schema = {'type': 'string'}
        validate(formData, schema)
        # throws ValueError on invalid format
        datetime.strptime(formData, '%H:%M')

    def parseForm(self, formData):
        dt = datetime.strptime(formData, '%H:%M')
        return dt.time()

# given map of form data, return a map of inputs 
def parse_widget_form_data(widgets, widgetFormData):
    inputs = {}
    for name, widget in widgets:
        formData = widgetFormData.get(name, None)
        if formData == None:
            inputs[name] = widget.default_value();
        else:
            inputs[name] = widget.parseForm(formData)
    return inputs
