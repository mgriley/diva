// reportId is a string like "report-0", "report-1", ...
function changeTab(reportId) {
    // hide all report tabs
    $('.report-tab').css('display', 'none');

    // display the components for the desired tab
    $('.' + reportId).css('display', 'block');

    // if the report can not yet been opened, load its default
    var index = parseInt(reportId.split('-')[1])
    var report = Reports.reportList[index]
    if (report.notYetSeen) {
        report.notYetSeen = false;
        report.update()
    }
}

$(document).ready(function() {
    // setup the buttons in report dropdown menu
    $('.report-option').on('click', function() {
        var reportId = $(this).attr('value');
        changeTab(reportId);
    });
        
    // init all reports
    var reportElements = $('.report');
    reportElements.each(function(index) {
        var reportElement = $(this);
        var report = Reports.create();
        
        // setup the report's user-defined widgets
        var widgetformParent = $('#widgetform-' + index).find('.user-widgets');
        report.widgets = Reports.Widgets.setupForm(widgetformParent);
    });

    // open the first tab
    // this must be called after the Reports state is configured
    $('.report-option').first().trigger('click');
});
