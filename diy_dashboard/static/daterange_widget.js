(function() {
    var widgetname = document.currentScript.dataset.widgetname;
    FigureWidgets.add(widgetname, FigureWidgets.inputTagWidget);

    // attach date-range picker to the input tag
    $('#' + widgetname).daterangepicker();
})();
