$(document).ready(function(){
$('#add_form_submit').click(function(){

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


  $.ajax({
    url: '/shipping/address/add/',
    method: 'POST',
    dataType: 'json',
    data: {
      'fullname': $('#fullname').val(),
      'phone_number': $('#phone_number').val(),
      'postal_address': $('#postal_address').val(),
      'postal_code': $('#postal_code').val(),
      'province': $('#province').val(),
      'city': $('#city').val()
    },
    success: function(res){
      if(res['status'] == 'ok'){
        top.location.href=$('#add_form_submit').attr('data-url');
      }else{
        $('#new_address_form').html(res.data)
      };
    },
  });


});


$('.my-delete-button').click(function(){

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

var address_id = $(this).attr('data-id')
var add = '#' + address_id


  $.ajax({
    url: '/shipping/address/delete/' + address_id + '/',
    method: 'POST',
    dataType: 'json',
    data: {
      'address_id': address_id
    },
    success: function(res){
      if(res['status'] == 'ok'){
        $(add).hide(2500)
      }
    },
  });

});

});
