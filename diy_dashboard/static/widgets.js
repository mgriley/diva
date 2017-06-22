var FigureWidgets = {};
(function(obj) {
    // map from name to widget
    obj.widgetMap = {};

    obj.add = function(name, widget) {
        obj.widgetMap[name] = widget;
    };

    obj.getValues = function() {
        var values = {};
        for (var name in obj.widgetMap) {
            values[name] = obj.widgetMap[name].getCurrentValue(name);
        }
        return values;
    };

    obj.resetToDefaults = function() {
        for (var name in obj.widgetMap) {
            obj.widgetMap[name].resetToDefault(name);
        }
    },

    // helper for defining widgets from HTML input forms
    // TODO: see if can get this code to work for all HTML forms
    obj.inputTagWidget = {
        resetToDefault: function(myName) {
            var input = document.getElementById(myName);
            input.value = input.defaultValue;
        },
        getCurrentValue: function(myName) {
            var input = document.getElementById(myName);
            return input.value;
        }
    };
})(FigureWidgets);

