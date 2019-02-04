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
