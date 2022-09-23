$(document).ready(function(){
    $('.delete').click(function(){
        $('.notification').hide()
    });
})

$(document).ready(function(){
    $(' #list' ).each(function(index){
        $(this).on('click', function(){
            let data = $(this).find('#id').text()
            
            let url = 'http://localhost:5000/course/watch/' + data
            window.location = url
        })
    });
});