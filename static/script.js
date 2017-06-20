$('#widgetform').ready(function() {
    $('#widgetform').on("submit", function(formEvent) {
        // prevent default action of get request
        formEvent.preventDefault();
        //console.log($(this).serialize());
        //var formData = $(this).serialize();
        // accumulate the values of the various widgets
        var valueMap = {};
        for (var key in widgetMap) {
            valueMap[key] = widgetMap[key].getCurrentValue(key);
        }
        console.log('form values: ' + valueMap);
        var currentPath = window.location.pathname;
        var callback = function(data) {
            console.log(data);
            $('.main').html(data);
        }
        $.ajax({
            url: currentPath,
            type: "POST",
            data: JSON.stringify(valueMap),
            contentType: "application/json",
            success: callback
        });
    });
});
