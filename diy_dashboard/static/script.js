function changeTab(mouseEvent, reportId) {
    // hide all report tabs
    var reportTabs = document.getElementsByClassName("report");
    for (var i = 0; i < reportTabs.length; ++i) {
        reportTabs[i].style.display = 'none';
    }

    // deselect all tab buttons
    var tabButtons = document.getElementsByClassName("tab-button");
    for (var i = 0; i < tabButtons.length; ++i) {
        var button = tabButtons[i];
        $(button).removeClass("active-button");
    }

    // display the desired tab
    var desiredTab = document.getElementById(reportId);
    desiredTab.style.display = "block";

    // add the active class to the button for the desired tab
    $(mouseEvent.target).addClass("active-button");
}

$(document).ready(function() {
    
    console.log('setting up reports');
    // init all reports
    var reportElements = $('.report');
    reportElements.each(function() {
        var reportElement = $(this);
        var report = Reports.create();
        
        // setup the report's user-defined widgets
        var widgetElements = $(reportElement).find('.user-widgets').children();
        widgetElements.each(function() {
            // extract name and type from the widget's outer div
            var element = $(this);
            var widgetType = element.data('widget-type');
            var widgetName = element.attr('name');
            // setup a widget of the requested type, and add to report
            var setupFunc = Reports.Widgets.setupMap[widgetType];
            var widget = setupFunc(element);
            report.widgets.add(widgetName, widget);
        });
    });

    // open the first report tab
    $('#button-0').click();
});
