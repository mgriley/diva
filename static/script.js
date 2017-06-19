$('#widgetform').on("submit", function(formEvent) {
    // prevent default action of get request
    formEvent.preventDefault();
    console.log($(this).serialize());
    var formData = $(this).serialize();
    var currentPath = window.location.pathname;
    console.log(currentPath);
    $.post(currentPath, formData, function(data) {
        console.log(data);
        $('.main').html(data);
    });
    //$('#figure').load(currentPath + " #figure", formData); 
    //$.get(currentPath, formData)
});
