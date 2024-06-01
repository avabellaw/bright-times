$(function() {
    $(".scroll-control[data-arrow='right']").click(function() {
        let target = $(this).data("target");
        scroll(target, 1);
    });

    $(".scroll-control[data-arrow='left']").click(function() {
        let target = $(this).data("target");
        scroll(target, -1);
    });

    function scroll(target, dir){
        let amnt = $(target).find(".row").find("div").innerWidth() * dir;
        console.log(amnt)
        let scrollAmt = $(target).scrollLeft() + amnt;
        $(target).animate({scrollLeft: scrollAmt}, 400);
    }
});