/*
Must convert strings to array buffers before passing to Blob b/c array
buffers are for arbitrary binary data.
see: https://stackoverflow.com/questions/16245767/creating-a-blob-from-a-base64-string-in-javascript
*/
var strToArrayBuffer = function(str) {
    var byteNums = new Array(str.length);
    for (var i = 0; i < str.length; ++i) {
        byteNums[i] = str.charCodeAt(i);
    }
    return new Uint8Array(byteNums);
};

// the 'utility' arg is the container div tag (class utility) as a JQuery object
Reports.Utilities.setupMap['basic'] = function(reportIndex, utilityIndex, utility) {

    // helper
    var submitData = function(data) {
        var onSuccess = function(responseData) {
            // the 'content' field of the response is the string of the 
            // file data encoded in base64
            var contentStr = window.atob(responseData['content']);
            var arrayBuffer = strToArrayBuffer(contentStr);
            var filename = responseData['filename'];
            var blob = new Blob([arrayBuffer]);
            saveAs(blob, filename);
        };
        var currentPath = window.location.pathname;
        var requestBody = {
            reportIndex: reportIndex,
            utilityIndex: utilityIndex,
            data: data
        };
         $.ajax({
            url: currentPath + 'utility',
            type: 'POST',
            data: JSON.stringify(requestBody),
            contentType: 'application/json',
            success: onSuccess
        });   
    };

    // setup the modal's widget form
    var modal = utility.find('.utility-modal');
    var utilityForm = $(modal).find('.utility-form');
    var widgets = Reports.Widgets.setupForm(utilityForm);

    // if the button takes no widgets, then clicking should submit
    // otherwise clicking should open the widget form for submitting
    var button = utility.find('.utility-button');
    $(button).on('click', function() {
        var requiresInput = widgets.widgetList.length > 0;
        if (requiresInput) {
            $(modal).modal('show');
        } else {
            submitData(widgets.getValues());        
        }
    });
    
    // upon submit, submit the widget values
    $(modal).find('.submit').on('click', function() {
        var data = widgets.getValues();
        submitData(data);
    });

    // upon reset, reset the widget values
    $(modal).find('.reset').on('click', function() {
        widgets.resetToDefaults();
    });
};

Reports.Utilities.setupMap['label'] = function() {
    // it's just a label, so no need for setup 
};
