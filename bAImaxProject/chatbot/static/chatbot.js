$(document).on('submit','#post-form',function(e){
    e.preventDefault();

    $.ajax({
        type: 'POST',
        url: '/send',
        data:{
            username: $(),
        }
    })
});