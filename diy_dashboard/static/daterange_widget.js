(function() {
    var widgetname = document.currentScript.dataset.widgetname;
    FigureWidgets.add(widgetname, FigureWidgets.inputTagWidget);

    // attach date-range picker to the input tag
    var inputTag = document.getElementById(widgetname);
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
        "startDate": inputTag.dataset.startdate,
        "endDate": inputTag.dataset.enddate,
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
    $('#' + widgetname).daterangepicker(pickerOptions, function(start, end, label) {
        return start.format('YYYY-MM-DD') + ' to ' + end.format('YYYY-MM-DD');
    });
})();
