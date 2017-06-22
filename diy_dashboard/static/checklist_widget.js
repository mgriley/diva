(function(widgetname) {
    FigureWidgets.add(widgetname, {
        getCurrentValue: function(name) {
            var elems = document.querySelectorAll('input[name=' + name + ']:checked');
            var selectedValues = [];
            for (var i = 0; i < elems.length; ++i) {
                selectedValues.push(elems[i].value);
            }
            return selectedValues;
        },
        resetToDefault: function(name) {
            var buttons = document.getElementsByName(name);
            for (var i = 0; i < buttons.length; ++i) {
                var b = buttons[i]
                b.checked = b.defaultChecked;
            }
        }
    });
})(document.currentScript.dataset.widgetname);
