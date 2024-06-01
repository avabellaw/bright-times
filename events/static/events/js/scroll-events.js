$(function() {
    $(".scroll-control[data-arrow='right']").click(function() {
        
        scroll($(this).data("target"), 100);
    });

    $(".scroll-control[data-arrow='left']").click(function() {
        let target = $(this).data("target");
        console.log(target)
        scroll(target, -100);
    });

    function scroll(target, scrollAmt){
        scrollAmt = $(target).scrollLeft() + scrollAmt;
        $(target).scrollLeft(scrollAmt);
    }
});