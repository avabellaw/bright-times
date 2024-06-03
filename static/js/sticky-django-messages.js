$(document).ready(function(){
    // Show bootstrap toasts on load
    $('.toast').toast('show');

    document.addEventListener('scroll', function (event) {
        if ($("#toast-container").visible() != true){
            $("#toast-container").addClass("position-fixed");
        }
    }, true /*Capture event*/);
});