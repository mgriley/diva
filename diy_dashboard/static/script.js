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
    for (var i = 0; i < reportElements.length; ++i) {
        var reportElement = reportElements[i];
        var report = Reports.create();
        
        // setup the report's widgets
        var widgetElements = $(reportElement).find('.user-widgets').children();
        for (var j = 0; j < widgetElements.length; ++j) {
            var widgetType = $(widgetElements[j]).data('widget-type');
            var setupFunc = Reports.Widgets.setupMap[widgetType];
            var widget = setupFunc(widgetElements[0]);
            report.widgets.add(widget);
        }
    }

    // open the first report tab
    $('#button-0').click();
});
