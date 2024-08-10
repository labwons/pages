


$(document).ready(function(){

    if (window.innerWidth <= 991) {
        $('#header').removeClass('header-fix');
        $('#header').css('margin-bottom', '10px');
    } else {
        $('#main').css('margin-top', $('#header').outerHeight(true) + 10);
    }

    $('.navbar-button').click(function(){
        if ($('#navbar').attr("class").includes("navbar-mobile")) {
            $('#navbar').removeClass('navbar-mobile');
            $(this).removeClass('fa-close').addClass('fa-bars');
        } else {
            $('#navbar').addClass('navbar-mobile');
            $(this).removeClass('fa-bars').addClass('fa-close');
        }
    })

})