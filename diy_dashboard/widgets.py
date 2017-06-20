from flask import render_template

class Widget:
    pass

class InputTagWidget:
    def generateHTML(self, widgetId, script_name='input_tag_widget.js'):
        return render_template('input_tag_widget.html',
                name=widgetId, attributes=self.attributes,
                script_name=script_name)

class TextWidget(InputTagWidget):
    def __init__(self, default="", placeholder=None):
        self.default = default
        self.attributes = {'type': 'text', 'value': default,
                'placeholder': placeholder}

    def parseForm(self, formData):
        return formData

class FloatWidget(InputTagWidget):
    def __init__(self, default=0, minVal=None, maxVal=None,
            step=0.001):
        self.default = default
        self.attributes = {'type': 'number', 'value': default,
                'min': minVal, 'max': maxVal, 'step': step}

    def parseForm(self, formData):
        try:
            return float(formData)
        except ValueError:
            return self.default

class IntWidget(FloatWidget):
    def __init__(self, default=0, minVal=None, maxVal=None):
        super(IntWidget, self).__init__(default, minVal, maxVal, step=1)

    def parseForm(self, formData):
        try:
            return int(formData)
        except ValueError:
            return self.default

class CheckBox(InputTagWidget):
    def __init__(self, default=False):
        self.default = default
        # TODO: figure out how to do specify checked or
        # unchecked as default (may need a checkbox.html),
        # which right now isn't used
        self.attributes = {'type': 'checkbox'}
        
    def generateHTML(self, widgetId, script_name=None):
        return super(CheckBox, self).generateHTML(widgetId,
            script_name='checkbox_widget.js')

    def parseForm(self, formData):
        return formData == 'True'

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
