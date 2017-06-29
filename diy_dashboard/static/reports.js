function newFigureWidgets() {
    var obj = {};

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
    return obj;
}

var Reports = {}
(function(obj) {
    obj.reportList = [];

    obj.create() = function() {
        var report = {widgets: newFigureWidgets()};
        obj.reportList.append(report);
    };
})(Reports);
