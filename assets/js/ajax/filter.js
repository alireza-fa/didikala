function FilterProduct(){

    filter_dict = {'brand': [], 'partner': [], 'category': [], 'color': []}
    var categories = document.getElementsByClassName('category');
    var brands = document.getElementsByClassName('brand');
    var partners = document.getElementsByClassName('partner');
    var colors = document.getElementsByClassName('color');
    var is_active = document.getElementById('switcher-1').checked;

    for(var i=0; i < categories.length; i++){
        if(categories[i].checked){
        filter_dict.category.push(categories[i].value);
        };
    };

    for (var i = 0; i < brands.length; i++){
        if(brands[i].checked){
        filter_dict.brand.push(brands[i].value);
        };
    };

    for (var i = 0; i < partners.length; i++){
        if(partners[i].checked){
        filter_dict.partner.push(partners[i].value);
        };
    };

    for(var i=0; i < colors.length; i++){
        if(colors[i].checked){
        filter_dict.color.push(colors[i].value);
        };
    };



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
    url: '/catalogue/filters/',
    method: 'POST',
    dataType: 'json',
    data: {
      'category': filter_dict.category,
      'partner': filter_dict.partner,
      'brand': filter_dict.brand,
      'color': filter_dict.color,
      'product_type_id': $('#submit_filters').attr('data-id'),
      'is_active': is_active
    },
    success: function(res){
      $('#product_tab').html(res.data)
    },
  });

  console.log(data);

}
