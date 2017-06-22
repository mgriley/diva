var widgetname = document.currentScript.dataset.widgetname;
FigureWidgets.add(widgetname, {
    getCurrentValue: function(name) {
        return document.querySelector('input[name=' + name + ']:checked').value;
    },
    resetToDefault: function(name) {
        var buttons = document.getElementsByName(name);
        for (var i = 0; i < buttons.length; ++i) {
            var b = buttons[i]
            b.checked = b.defaultChecked;
        }
    }
});
