(function() {
    var currentScript = document.currentScript;
    console.log('executing text widget script');
    $('document').ready(function() {
        var widgetName = currentScript.dataset.widgetname;
        console.log(widgetName)
        widgetMap[widgetName] = {
            getCurrentValue: function(myName) {
                var textInput = document.getElementById(myName);
                return textInput.value;
            }
        };
    });
})();
