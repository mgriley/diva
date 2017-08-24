// the 'utility' arg is the container div tag (class utility) as a JQuery object
Reports.Utilities.setupMap['basic'] = function(reportIndex, utilityIndex, utility) {
    console.log('setting up simple util');

    // helper
    var submitData = function(data) {
        var onSuccess = function(responseData) {
            console.log('received data');
            console.log(responseData);
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

    // upon clicking the button, show the modal
    var button = utility.find('.utility-button');
    $(button).on('click', function() {
        console.log('showing');
        $(modal).modal('show');
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
