// the 'util' arg is the container div tag (class utility) as a JQuery object

Reports.Utilities.setupMap['export'] = function(reportIndex, utilityIndex, utility) {
    console.log('setting up simple util');            
    var button = utility.find('.utility-button');
    var onSuccess = function(data) {
        console.log('received data');
        console.log(data);
    };
    var currentPath = window.location.pathname;
    var requestBody = {
        reportIndex: reportIndex,
        utilityIndex: utilityIndex,
        data: {}
    };
    $(button).on('click', function() {
        console.log('btn clicked');
        $.ajax({
            url: currentPath + 'utility',
            type: 'POST',
            data: JSON.stringify(requestBody),
            contentType: 'application/json',
            success: onSuccess
        });
    });
};
