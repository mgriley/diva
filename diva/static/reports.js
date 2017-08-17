function newFigureWidgets() {
    var obj = {};

    // List of all Widget objects, which are
    // the objects returned by the function in setupMap
    // for a widget of its type
    obj.widgetList = [];

    /*
    widget is the Widget object returned from the function in the setupMap for
    a widget of this type.
    */
    obj.add = function(widget) {
        obj.widgetList.push(widget);
    };

    /*
    Get a list of widget values from list of widgets
    */
    obj.getValues = function() {
        var values = [];
        for (var i = 0; i < obj.widgetList.length; ++i) {
            values.push(obj.widgetList[i].getCurrentValue());
        }
        return values;
    };

    obj.resetToDefaults = function() {
        for (var i = 0; i < obj.widgetList.length; ++i) {
            obj.widgetList[i].resetToDefault();
        }
    };

    return obj;
};

/*
Return a Report object. There is one Report for every function 
decorated/registered with the Diva object.
*/
function newReport(reportIndex) {
    var obj = {
        reportIndex: reportIndex,
        // a Widgets object, as defined above
        widgets: newFigureWidgets()
    };
    
    /*
    Use the current values of the widgets to update the HTML displayed 
    for this report.
    */
    obj.update =  function() {
        // get the current values of the widgets
        valueArray = obj.widgets.getValues();
        var updateRequest = {
            reportIndex: obj.reportIndex,
            widgetValues: valueArray
        };
        console.log('form values: ' + JSON.stringify(updateRequest));
        var currentPath = window.location.pathname;

        // on success, replace the report's HTML with the response
        var callback = function(data) {
            var figureId = '#figure-' + obj.reportIndex;
            $(figureId).html(data);
        }
        $.ajax({
            url: currentPath + 'update',
            type: "POST",
            data: JSON.stringify(updateRequest),
            contentType: "application/json",
            success: callback
        });    
    };

    // the id of the widget form for this Report
    var widgetFormId = '#widgetform-' + obj.reportIndex;

    // update the figure/HTML on submit
    $(widgetFormId).on("submit", function(formEvent) {
        // prevent default get request
        console.log('submitting');
        formEvent.preventDefault();
        obj.update();
    });

    // Reset the widget form and the displayed figure to the default
    // values of the widgets
    // NA if no user-defined widgets
    $(widgetFormId).on("reset", function(formEvent) {
        console.log('resetting');
        formEvent.preventDefault();
        obj.widgets.resetToDefaults();
        obj.update();
    });

    return obj;
}

// Global state
var Reports = {};
(function(obj) {
    // list of Report objects
    obj.reportList = [];

    obj.Widgets = {
        /*
        Map from widget type (which is the class name in widgets.py) to setup function
        A setup function takes the widget's parent container (see class widgetcontainer in index.html)
        as a JQuery object, and returns an object of the following form:
        {
            resetToDefault: noargs function that resets the widget to its default value
            getCurrentValue: noargs function that returns the current value of the widget
        }
        The functions in the returned object keep a reference to the given JQuery object (closure)
        */
        setupMap: {}
    };

    /*
    Create a new Report object, and add it to the list
    */
    obj.create = function() {
        var reportIndex = obj.reportList.length;
        var report = newReport(reportIndex);
        obj.reportList.push(report);
        return report;
    };
})(Reports);
