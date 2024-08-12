


$(document).ready(function(){

    fetch('../template/header.html')
    .then(response => response.text())
    .then(data => {
        document.getElementById('header').innerHTML = data;
    })

    if (window.innerWidth <= 991) {
        $('#header').removeClass('header-fix');
    } 
    
    if ($('#header').attr("class").includes("header-fix")) {
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