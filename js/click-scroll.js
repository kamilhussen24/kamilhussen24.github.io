var sectionArray = [1, 2, 3, 4, 5];

$.each(sectionArray, function(index, value){
    
    // Scroll Event
    $(document).scroll(function(){
        var offsetSection = $('#section_' + value).offset().top - 90;
        var docScroll = $(document).scrollTop();
        var docScroll1 = docScroll + 1;

        if ( docScroll1 >= offsetSection ){
            $('.navbar-nav .nav-item .nav-link').removeClass('active');
            $('.navbar-nav .nav-item .nav-link:link').addClass('inactive');  
            $('.navbar-nav .nav-item .nav-link').eq(index).addClass('active');
            $('.navbar-nav .nav-item .nav-link').eq(index).removeClass('inactive');
        }
    });

    // Click Event (শুধু যদি section থাকে, বাইরের লিংকে নয়)
    var link = $('.click-scroll').eq(index);
    var href = link.attr('href');

    if (href && href.startsWith('#section_')) {
        link.click(function(e){
            e.preventDefault();
            var offsetClick = $('#section_' + value).offset().top - 90;
            $('html, body').animate({
                'scrollTop': offsetClick
            }, 300);
        });
    }
});

$(document).ready(function(){
    $('.navbar-nav .nav-item .nav-link:link').addClass('inactive');    
    $('.navbar-nav .nav-item .nav-link').eq(0).addClass('active');
    $('.navbar-nav .nav-item .nav-link:link').eq(0).removeClass('inactive');
});
