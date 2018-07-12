//Scripts for editGroups page


$(document).ready(function() {

    // JQuery code to be added in here.
    $("li").hover(function () {
        $(this).find("button.del_btn").css("visibility","visible");
    }, function () {
        $(this).find("button.del_btn").css("visibility","hidden");
    });

    //show submit button on focus
    $(".add_grp_input").focus(function(){
        $(this).css("width","90%");
        $("#submit_add_grp").css("display","inline")
    });

    $(".add_grp_input").focusout(function(){
        $(this).css("width","100%");
        $("#submit_add_grp").css("display","none")
    });

    
    $('.del_btn').click(function(e){
        $("#myModal").modal();    
    });
});


function confirm_delete(this){
    //$("#myModal").modal();
    $(this).parent().html("HELLO")
    console.log(group)
    $("#modalText").html(group);
}
