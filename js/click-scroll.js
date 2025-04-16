//jquery-click-scroll
//by syamsul'isul' Arifin (Updated by Kamil & ChatGPT)

var sectionArray = [1, 2, 3, 4, 5];

// SCROLL EVENT
$(document).scroll(function () {
    var docScroll = $(document).scrollTop() + 1;

    $.each(sectionArray, function (index, value) {
        var offsetSection = $('#section_' + value).offset().top - 90;

        if (docScroll >= offsetSection) {
            $('.navbar-nav .nav-item .nav-link').removeClass('active');
            $('.navbar-nav .nav-item .nav-link:link').addClass('inactive');
            $('.navbar-nav .nav-item .nav-link').eq(index).addClass('active').removeClass('inactive');
        }
    });
});

// CLICK EVENT
$.each(sectionArray, function (index, value) {
    var selector = $('.click-scroll').eq(index);
    var href = selector.attr('href');

    if (href && href.startsWith('#section_')) {
        selector.click(function (e) {
            e.preventDefault();
            var offsetClick = $('#' + 'section_' + value).offset().top - 90;
            $('html, body').animate({
                'scrollTop': offsetClick
            }, 300);
        });
    }
});

// INITIAL ACTIVE CLASS
$(document).ready(function () {
    $('.navbar-nav .nav-item .nav-link:link').addClass('inactive');
    $('.navbar-nav .nav-item .nav-link').eq(0).addClass('active').removeClass('inactive');
});
