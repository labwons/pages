


$(document).ready(function(){

    if (window.innerWidth <= 991) {
        $('#header').removeClass('header-fix');
    } else {
        $('#main').css('margin-top', $('#header').outerHeight(true));
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