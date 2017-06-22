from flask import render_template
import time

class Widget:
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

# given map of form data, return a map of inputs 
def parse_widget_form_data(widgets, widgetFormData):
    inputs = {}
    for keyVal in widgets:
        name = keyVal[0]
        widget = keyVal[1]
        formData = widgetFormData.get(name, None)
        if formData == None:
            inputs[name] = widget.default;
        else:
            inputs[name] = widget.parseForm(formData)
    return inputs
