$(document).ready(function(){

$('#next_page').click(function(){

if($('#next_page').attr('data-address') == 'false'){
alert('شما آدرسی را ثبت نکرده اید');
top.location.href=$('#next_page').attr('data-url')
}else{
top.location.href=$('next_page').attr('data-next')}
});

$('.change-active-address-button').click(function(){

  $.ajax({
    url: '/shipping/address/change_active_address/' + $(this).attr('data-id') + '/',
    method: 'GET',
    dataType: 'json',
    data: {
      'address_id': $(this).attr('data-id')
    },
    success: function(res){
      if(res['status'] == 'ok'){
        top.location.href='/shopping/'
      };
    },

  });

});

});