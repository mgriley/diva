function changeTab(mouseEvent, reportId) {
    // hide all report tabs
    var reportTabs = document.getElementsByClassName("report");
    for (var i = 0; i < reportTabs.length; ++i) {
        reportTabs[i].style.display = 'none';
    }

    // display the desired tab
    var desiredTab = document.getElementById(reportId);
    desiredTab.style.display = "block";
}

$('#body').ready(function() {
    console.log('clicking first tab button');
    // open the first report tab
    $('#button-0').click();
});

// TODO: move this into widgets.js so that it is all in one place
/*$('#widgetform').ready(function() {*/

    //var updateReport = function() {
        //valueMap = FigureWidgets.getValues();
        //console.log('form values: ' + JSON.stringify(valueMap));
        //var currentPath = window.location.pathname;
        //var callback = function(data) {
            //console.log(data);
            //$('#figure').html(data);
        //}
        //$.ajax({
            //url: currentPath,
            //type: "POST",
            //data: JSON.stringify(valueMap),
            //contentType: "application/json",
            //success: callback
        //});    
    //}

    //$('#widgetform').on("submit", function(formEvent) {
        //// prevent default action of get request
        //formEvent.preventDefault();
        //updateReport();
    //});

    //$('#widgetform').on("reset", function(formEvent) {
        //console.log('resetting');
        //formEvent.preventDefault();
        //FigureWidgets.resetToDefaults();
        //updateReport();
    //});
/*});*/
