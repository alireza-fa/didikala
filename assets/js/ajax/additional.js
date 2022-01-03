$(document).ready(function(){
$('.additional_button').click(function(){


var address_id = $(this).attr('data-id');

  $.ajax({
    url: '/shipping/address/edit/' + address_id + '/',
    method: 'GET',
    dataType: 'json',
    data: {
    },
    success: function(res){
      if(res['status'] == 'ok'){
        $(add).hide(2500)
      }else{
        $('#edit_address_form').html(res.data)
      }
    },
  });

});

$('#edit_form_button').click(function(){


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
    url: '/shipping/address/edit/save/',
    method: 'POST',
    dataType: 'json',
    data: {
      'fullname': $('#fullname_edit').val(),
      'phone_number': $('#phone_number_edit').val(),
      'postal_address': $('#postal_address_edit').val(),
      'postal_code': $('#postal_code_edit').val(),
      'province': $('#province_edit').val(),
      'city': $('#city_edit').val()
    },
    success: function(res){
      if(res['status'] == 'ok'){
        top.location.href=$('#edit_form_button').attr('data-url');
      }else{
        $('#edit_address_form').html(res.data)
      };
    },
  });

});

});
