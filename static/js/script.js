// (function(){
//     let csrftoken = Cookies.get('csrftoken');
//     $ajaxSetup(
//         {
//             headers:{'X-CSRFToken':csrftoken}
//         });
//
// })();
let csrftoken = Cookies.get('csrftoken');
    $.ajaxSetup({
        headers: {"X-CSRFToken": csrftoken}
    });

$(".set_rating").submit(function(e){
        e.preventDefault();
        var url = $(this).attr('action');
        var data = $(this).serialize();
        $.post(
            url,
            data,
            function(response){
                window.location = response.location;
            }
        );
})
$(document).ready(function () {
    var qty = 0;
    $('.quantity-right-plus').click(function (e) {
        // Stop acting like a button
        e.preventDefault();
        // Get the field name
        var qty = parseInt($('#qty').val());
        // If is not undefined
        $('#qty').val(qty + 1);
        // Increment
    });

    $('.quantity-left-minus').click(function (e) {
        // Stop acting like a button
        e.preventDefault();
        // Get the field name
        var qty = parseInt($('#qty').val());
        // If is not undefined
        // Increment
        if (qty > 0) {
            $('#qty').val(qty - 1);
        }
    });

});
