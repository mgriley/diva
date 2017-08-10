function changeTab(reportId) {
    // hide all report tabs
    $('.report-tab').css('display', 'none');

    // display the components for the desired tab
    $('.' + reportId).css('display', 'block');
}

$(document).ready(function() {
    // setup the report selector
    $('.report-option').on('click', function() {
        var reportId = $(this).attr('value');
        changeTab(reportId);
        //$('.dropdown-content').css('display', 'none');
    });

    // open the first tab
    $('.report-option').first().trigger('click');
    
    console.log('setting up reports');
    // init all reports
    var reportElements = $('.report');
    reportElements.each(function(index) {
        var reportElement = $(this);
        var report = Reports.create();
        
        // setup the report's user-defined widgets
        var widgetElements = $('#widgetform-' + index).find('.user-widgets').children();
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
});
