// TODO: left off here. Figure out how to get the current report, then we're good
(function(widgetname) {
    var currentReport = getCurrentReport();
    currentReport.widgets.add(widgetname, FigureWidgets.inputTagWidget);
})(document.currentScript.dataset.widgetname);
