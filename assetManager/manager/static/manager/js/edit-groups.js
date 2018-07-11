//Scripts for editGroups page


$(document).ready(function() {

    // JQuery code to be added in here.
    $("li").hover(function () {
        $(this).find("button.del_btn").css("visibility","visible");
    }, function () {
        $(this).find("button.del_btn").css("visibility","hidden");
    });
});
