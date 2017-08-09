function changeTab(reportId) {
    // hide all report tabs
    $('.report-tab').css('display', 'none');

    // display the components for the desired tab
    $('.' + reportId).css('display', 'block');
}

$(document).ready(function() {
    // setup the report selector
    $('#report-selector').on('change', function() {
        var reportId = $(this).find('option:selected').attr('value');
        changeTab(reportId);
    });

    // open the first tab
    $('#report-selector').trigger('change');

    // TODO: use a better report selector dropdown menu
    
    
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
