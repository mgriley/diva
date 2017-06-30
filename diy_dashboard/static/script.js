function changeTab(mouseEvent, reportId) {
    // hide all report tabs
    var reportTabs = document.getElementsByClassName("report");
    for (var i = 0; i < reportTabs.length; ++i) {
        reportTabs[i].style.display = 'none';
    }

    // deselect all tab buttons
    var tabButtons = document.getElementsByClassName("tab-button");
    for (var i = 0; i < tabButtons.length; ++i) {
        var button = tabButtons[i];
        $(button).removeClass("active-button");
    }

    // display the desired tab
    var desiredTab = document.getElementById(reportId);
    desiredTab.style.display = "block";

    // add the active class to the button for the desired tab
    $(mouseEvent.target).addClass("active-button");
}

$('#body').ready(function() {
    console.log('clicking first tab button');
    // open the first report tab
    $('#button-0').click();
});

