from django import forms
from shipping.models import Address

error_msg = {
    "valid": 'ایمیل وارد شده معتبر نمیباشد',
    "required": 'این فیلد اجباری است',
}


class AddAddressForm(forms.Form):
    fullname = forms.CharField(
        widget=forms.TextInput(attrs={"class": 'input-ui pr-2 text-right', "placeholder": 'نام خود را وارد نمایید', "id": 'fullname'}),
        error_messages=error_msg
    )
    phone_number = forms.CharField(
        widget=forms.TextInput(attrs={"class": 'input-ui pl-2 dir-ltr text-left', "placeholder": '09xxxxxxxxx', "id": 'phone_number'}),
        error_messages=error_msg
    )
    postal_address = forms.CharField(
        widget=forms.Textarea(attrs={"class": 'input-ui pr-2 text-right', "placeholder": ' آدرس تحویل گیرنده را وارد نمایید', "id": 'postal_address'}),
        error_messages=error_msg
    )
    postal_code = forms.CharField(
        widget=forms.TextInput(attrs={"class": 'input-ui pl-2 dir-ltr text-left placeholder-right', "placeholder": 'کد پستی را بدون خط تیره بنویسید', "id": 'postal_code'}),
        error_messages=error_msg
    )
    province = forms.CharField(
        widget=forms.TextInput(attrs={"class": 'input-ui pr-2 text-right', "id": 'province'}),
        error_messages=error_msg
    )
    city = forms.CharField(
        widget=forms.TextInput(attrs={"class": 'input-ui pl-2 dir-ltr text-left placeholder-right', "id": 'city'}),
        error_messages=error_msg
    )

    def save(self, user):
        active_addresses = Address.objects.filter(user=user, is_active=True)
        for ac_add in active_addresses:
            ac_add.is_active = False
            ac_add.save()
        cd = self.cleaned_data
        address = Address(
            user=user, fullname=cd['fullname'], phone_number=cd['phone_number'], province=cd['province'],
            city=cd['city'], postal_address=cd['postal_address'], postal_code=cd['postal_code'], is_active=True
        )
        address.save()


class EditAddressForm(forms.Form):
    fullname = forms.CharField(
        widget=forms.TextInput(
            attrs={"class": 'input-ui pr-2 text-right', "placeholder": 'نام خود را وارد نمایید', "id": 'fullname_edit'}),
        error_messages=error_msg
    )
    phone_number = forms.CharField(
        widget=forms.TextInput(attrs={"class": 'input-ui pl-2 dir-ltr text-left', "placeholder": '09xxxxxxxxx', "id": 'phone_number_edit'}),
        error_messages=error_msg
    )
    postal_address = forms.CharField(
        widget=forms.Textarea(
            attrs={"class": 'input-ui pr-2 text-right', "placeholder": ' آدرس تحویل گیرنده را وارد نمایید', "id": 'postal_address_edit'}),
        error_messages=error_msg
    )
    postal_code = forms.CharField(
        widget=forms.TextInput(attrs={"class": 'input-ui pl-2 dir-ltr text-left placeholder-right',
                                      "placeholder": 'کد پستی را بدون خط تیره بنویسید', "id": 'postal_code_edit'}),
        error_messages=error_msg
    )
    province = forms.CharField(
        widget=forms.TextInput(attrs={"class": 'input-ui pr-2 text-right', "id": 'province_edit'}),
        error_messages=error_msg
    )
    city = forms.CharField(
        widget=forms.TextInput(attrs={"class": 'input-ui pl-2 dir-ltr text-left placeholder-right', "id": 'city_edit'}),
        error_messages=error_msg
    )

    def edit(self, user, address):
        active_addresses = Address.objects.filter(user=user, is_active=True)
        for ac_add in active_addresses:
            ac_add.is_active = False
            ac_add.save()
        cd = self.cleaned_data
        if cd['fullname']:
            address.fullname = cd['fullname']
        if cd['phone_number']:
            address.phone_number = cd['phone_number']
        if cd['postal_address']:
            address.postal_address = cd['postal_address']
        if cd['postal_code']:
            address.postal_code = cd['postal_code']
        if cd['province']:
            address.province = cd['province']
        if cd['city']:
            address.city = cd['city']
        address.is_active = True
        address.save()
