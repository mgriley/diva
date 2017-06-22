// the things I do for javascript...
(function(widgetName) {
    FigureWidgets.add(widgetName, FigureWidgets.inputTagWidget);
    $('#widgetform').ready(function() {
        console.log('ready');
        var id = '#' + widgetName;
        $('#widgetform').on('input', id, function(changeEvent) {
            console.log('changing the slider value')
            var currentVal = $(id).val();
            $('#current-' + widgetName).text(currentVal);
        });
    });   
})(document.currentScript.dataset.widgetname);


