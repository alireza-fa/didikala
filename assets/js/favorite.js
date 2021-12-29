$('#favorite_button').click(function(){

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
var csrftoken = getCookie('csrftoken');
function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});

var product_id = $('#favorite_button').attr('data-product')
var class_name = $('#favorite_button').attr('class')


if(class_name == 'add-favorites'){
    var url = '/catalogue/favorite/'
    var btn_class = 'add-favorites favorites'
}else{
    var url = '/catalogue/no_favorite/'
    var btn_class = 'add-favorites'
}

    $.ajax({
        url: url,
        method: 'POST',
        data: {
            'product_id': product_id
        },
        success: function(data){
            if(data['status'] == 'ok'){
                $('#favorite_button').attr({"class": btn_class})
            }
        }
    });

});
