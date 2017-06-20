console.log('executing text widget script');
var widgetname = document.currentScript.dataset.widgetname;
console.log(widgetname);
FigureWidgets.add(widgetname, {
    getCurrentValue: function(myName) {
        var textInput = document.getElementById(myName);
        return textInput.value;
    }
});
