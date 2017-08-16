/*
Setup functions for all widget types:
See the Reports object in reports.js for an explanation of 
setupMap
*/

// Helpers:

var resetToDefaultChecked = function(element) {
    var defaultVal = element.prop('defaultChecked');
    element.prop('checked', defaultVal);
};

var resetAllToDefaultChecked = function(elements) {
    elements.each(function() {
        resetToDefaultChecked($(this));
    });
}

// index into the children of a jquery obj and return the result
// as a jquery obj
var getChild = function(parentObj, index) {
    return $(parentObj.children().toArray(index));
}

// The setup function for a widget that simply wraps an input tag
var setupInputTagWidget = function(widget) {
    // the input tag is the first and only child of the widget's
    // div parent/container
    var input = widget.find(".input-tag-widget");
    return {
         resetToDefault: function() {
            input.val(input.prop('defaultValue'));
        },
        getCurrentValue: function() {
            return input.val();
        }   
    };
};

// Setup functions for the built-in widgets:
// Note: the key value in the setup map must match the name of the 
// widget class (as defined in widgets.py) exactly

// setup all types that use input tags
var inputTagTypes = ['String', 'Float', 'Int', 'Color', 'Date', 'Time']
for (var i = 0; i < inputTagTypes.length; ++i) {
    widgetType = inputTagTypes[i]
    Reports.Widgets.setupMap[widgetType] = function(widget) {
        return setupInputTagWidget(widget);
    };
}

Reports.Widgets.setupMap['Bool'] = function(widget) {
    return {
        getCurrentValue: function() {
            return getChild(widget, 0).is(':checked');
        },
        resetToDefault: function() {
            var input = getChild(widget, 0);
            resetToDefaultChecked(input);
        }
    };
};

Reports.Widgets.setupMap['SelectOne'] = function(widget) {
    return {
        getCurrentValue: function() {
            return widget.children().filter('input:checked').val();
        },
        resetToDefault: function() {
            var buttons = widget.children().filter('input');
            resetAllToDefaultChecked(buttons);
        }
    }
};

Reports.Widgets.setupMap['SelectSubset'] = function(widget) {
    return {
        getCurrentValue: function() {
            // get a list of the values of each checked input tag
            var checkedElems = widget.children().filter(':checked');
            var selectedValues = checkedElems.map(function() {
                return $(this).val();
            }).get();
            return selectedValues;
        },
        resetToDefault: function() {
            var buttons = widget.children();
            resetAllToDefaultChecked(buttons);
        }
    }
};

Reports.Widgets.setupMap['Slider'] = function(widget) {
    var inputElement = widget.children().filter('.slider-input');
    var textElement = widget.children().filter('.slider-value');
    // the text element should always display the slider's 
    // current value
    inputElement.on('input', function(changeEvent) {
        var currentVal = inputElement.val();
        textElement.text(currentVal);
    });
    return {
        resetToDefault: function() {
            inputElement.val(inputElement.prop('defaultValue'));
            // force the text to update
            inputElement.trigger('input');
        },
        getCurrentValue: function() {
            return inputElement.val();
        }
    };
};

Reports.Widgets.setupMap['DateRange'] = function(widget) {
    // attach date-range picker to the input tag
    var inputTag = widget.find(".input-tag-widget")
    pickerOptions = {
        "showDropdowns": true,
        "ranges": {
            'Today': [moment(), moment()],
           'Yesterday': [moment().subtract(1, 'days'), moment().subtract(1, 'days')],
           'Last 7 Days': [moment().subtract(6, 'days'), moment()],
           'Last 30 Days': [moment().subtract(29, 'days'), moment()],
           'This Month': [moment().startOf('month'), moment().endOf('month')],
           'Last Month': [moment().subtract(1, 'month').startOf('month'), moment().subtract(1, 'month').endOf('month')]
        },
        "locale": {
            "format": "YYYY-MM-DD",
            "separator": " to ",
            "applyLabel": "Apply",
            "cancelLabel": "Cancel",
            "fromLabel": "From",
            "toLabel": "To",
            "customRangeLabel": "Custom",
            "weekLabel": "W",
            "daysOfWeek": [
                "Su",
                "Mo",
                "Tu",
                "We",
                "Th",
                "Fr",
                "Sa"
            ],
            "monthNames": [
                "January",
                "February",
                "March",
                "April",
                "May",
                "June",
                "July",
                "August",
                "September",
                "October",
                "November",
                "December"
            ],
            "firstDay": 1
        },
        "linkedCalendars": false,
        "alwaysShowCalendars": true,
        "startDate": inputTag.data('startdate'),
        "endDate": inputTag.data('enddate'),
        "drops": "down"
    };
    // min and max date not implemented into the data-range widget yet
    // It doesn't seem very useful
    /*
    if (inputTag.dataset.mindate) {
        pickerOptions.minDate = inputTag.dataset.mindate; 
    }
    if (inputTag.dataset.maxdate) {
        pickerOptions.maxDate = inputTag.dataset.maxdate;
    }
    */
    inputTag.daterangepicker(pickerOptions, function(start, end, label) {
        return start.format('YYYY-MM-DD') + ' to ' + end.format('YYYY-MM-DD');
    });
    return {
         resetToDefault: function() {
            inputTag.val(inputTag.prop('defaultValue'));
        },
        getCurrentValue: function() {
            return inputTag.val().split(' to ');
        }   
    };
};

Reports.Widgets.setupMap['Date'] = function(widget) {
    // via Bootstrap's datepicker
    $(widget).find('.input-tag-widget').datepicker();
    return setupInputTagWidget(widget);
};

Reports.Widgets.setupMap['Time'] = function(widget) {
    // via Bootstrap timepicker. For options
    // see: https://jdewit.github.io/bootstrap-timepicker/
    $(widget).find('.input-tag-widget').timepicker({
        'defaultTime': false,
        // 12 vs 24hr mode
        'showMeridian': false
    });
    return setupInputTagWidget(widget);
};
