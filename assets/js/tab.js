$(document).ready(function(){
    $('.ah-tab-item').click(function(){

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

var filter_tab = $(this).attr('data-filter')
var page_obj = $(this).attr('data-product')

  $.ajax({
    url: '/catalogue/filter_tab/',
    method: 'POST',
    dataType: 'json',
    data: {
      'filter_tab': filter_tab,
      'page_obj': $(this).attr('data-product')
    },
    success: function(res){
      console.log(res)
      $('#product_tab').html(res.data)
    },
  });

    });
});
