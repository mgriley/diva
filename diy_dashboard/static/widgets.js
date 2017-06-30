/*
Setup functions for all widget types
*/

Reports.Widgets.setupMap['InputTag'] = function() {
    return Reports.inputTagWidget;
};

Reports.Widgets.setupMap['Bool'] = function() {
    return {
        getCurrentValue: function(name) {
            return $('#' + name).is(':checked');
        },
        resetToDefault: function(name) {
            var input = document.getElementById(name);
            input.checked = input.defaultChecked;
        }
    };
};

Reports.Widgets.setupMap['SelectOne'] = function() {
    return 
    {
        getCurrentValue: function(name) {
            return document.querySelector('input[name=' + name + ']:checked').value;
        },
        resetToDefault: function(name) {
            var buttons = document.getElementsByName(name);
            for (var i = 0; i < buttons.length; ++i) {
                var b = buttons[i]
                b.checked = b.defaultChecked;
            }
        }
    }
};

Reports.Widgets.setupMap['SelectSubset'] = function() {
    return 
    {
        getCurrentValue: function(name) {
            var elems = document.querySelectorAll('input[name=' + name + ']:checked');
            var selectedValues = [];
            for (var i = 0; i < elems.length; ++i) {
                selectedValues.push(elems[i].value);
            }
            return selectedValues;
        },
        resetToDefault: function(name) {
            var buttons = document.getElementsByName(name);
            for (var i = 0; i < buttons.length; ++i) {
                var b = buttons[i]
                b.checked = b.defaultChecked;
            }
        }
    }
};

Reports.Widgets.setupMap['Slider'] = function(widgetElement) {
    var children = widgetElement.children();
    var inputElement = children[0];
    var textElement = children[1];
    inputElement.on('input', function(changeEvent) {
        console.log('changing the slider value')
        var currentVal = inputElement.val();
        textElement.text(currentVal);
    });
    return Reports.inputTagWidget;
};

Reports.Widgets.setupMap['DateRange'] = function(widgetElement) {
    // attach date-range picker to the input tag
    var inputTag = widgetElement.children()[0]
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
        "startDate": inputTag.data(startdate),
        "endDate": inputTag.data(enddate),
        "drops": "down"
    };
    // min and max date not implemented into the data-range widget yet
    // It doesn't seem useful
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
    return Reports.inputTagWidget;
};


