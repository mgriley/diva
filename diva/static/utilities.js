// the 'utility' arg is the container div tag (class utility) as a JQuery object
Reports.Utilities.setupMap['basic'] = function(reportIndex, utilityIndex, utility) {
    console.log('setting up simple util');

    // helper
    var submitData = function(data) {
        var onSuccess = function(responseData) {
            console.log(responseData);
            // The server should have responsed with a file, so save it
            // content is in base64, so decode
            var content = atob(responseData['content']);
            var filename = responseData['filename'];
            var file = new File([content], filename);
            saveAs(file);
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
        console.log('submitting');
        var data = widgets.getValues();
        submitData(data);
    });

    // upon reset, reset the widget values
    $(modal).find('.reset').on('click', function() {
        console.log('resetting');
        widgets.resetToDefaults();
    });
};
