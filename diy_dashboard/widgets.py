from flask import render_template

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
