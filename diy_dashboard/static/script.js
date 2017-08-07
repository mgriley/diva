function changeTab(mouseEvent, reportId) {
    // hide all report tabs
    $('.report').css('display', 'none');

    // deselect all tab buttons
    $('.tab-button').removeClass('active-button');

    // display the desired tab
    $('#' + reportId).css('display', 'block');

    // add the active class to the button for the desired tab
    // (so that it can be emphasized with CSS)
    $(mouseEvent.target).addClass("active-button");
}

$(document).ready(function() {
    // setup the tab buttons
    var tabButtons = $('.tab-button');
    tabButtons.each(function(index) {
        var button = $(this);
        button.click(function(mouseEvent) {
            mouseEvent.preventDefault();
            var desiredReportId = 'report-' + index;
            changeTab(mouseEvent, desiredReportId);
        });
    });
    
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
    var firstButton = $(tabButtons[0])
    firstButton.click();
});
