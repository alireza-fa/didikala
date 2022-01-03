from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.views.decorators.http import require_POST, require_http_methods, require_GET
from .forms import AddAddressForm, EditAddressForm
from .models import Address


@login_required
def add_address(request):
    if request.method == 'POST':
        form = AddAddressForm(request.POST)
        if form.is_valid():
            form.save(request.user)
            t = render_to_string('shipping/ajax/row.html', {'addresses': Address.objects.filter(user=request.user)})
            url = '/accounts/profile/address/'
            return JsonResponse({"data": t, "url": url, "status": 'ok'}, safe=False)
        else:
            t = render_to_string('shipping/ajax/new_address_form.html', {"form": form})
            return JsonResponse({"data": t, "status": 'bad'}, safe=False)
    else:
        form = AddAddressForm()
    return render(request, 'shipping/add_address.html', {"form": form})


@login_required
@require_http_methods(request_method_list=['GET'])
def edit_address(request, address_id=None):
    if request.method == 'GET':
        address = get_object_or_404(Address, id=address_id, user=request.user)
        global add_id
        add_id = address_id
        form = EditAddressForm(initial={
            "fullname": address.fullname, "phone_number": address.phone_number,
            "postal_address": address.postal_address, "postal_code": address.postal_code,
            "province": address.province, "city": address.city
        })
        t = render_to_string('shipping/ajax/edit_address_form.html', {"form": form})
        return JsonResponse({"data": t, "status": 'bad'}, safe=False)
    if request.method == 'POST':
        form = EditAddressForm(request.POST)
        if form.is_valid():
            form.edit(user=request.user, address=add_id)
            return JsonResponse({"status": 'ok'})
        else:
            t = render_to_string('shipping/ajax/edit_address_form.html', {"form": form})
            return JsonResponse({"data": t, "status": 'bad'}, safe=False)


@login_required
@require_POST
def edit_address_save(request):
    form = EditAddressForm(request.POST)
    if form.is_valid():
        address = get_object_or_404(Address, id=add_id, user=request.user)
        form.edit(user=request.user, address=address)
        return JsonResponse({"status": 'ok'})
    else:
        t = render_to_string('shipping/ajax/edit_address_form.html', {"form": form})
        return JsonResponse({"data": t, "status": 'bad'}, safe=False)


@login_required
@require_POST
def delete_address(request, address_id):
    address = get_object_or_404(Address, id=address_id, user=request.user)
    address.delete()
    return JsonResponse({"status": 'ok'})


def active_address(request, address_id):
    ac_address = get_object_or_404(Address, is_active=True, user=request.user)
    ac_address.is_active = False
    ac_address.save()
    address = get_object_or_404(Address, id=address_id, user=request.user, is_active=False)
    address.is_active = True
    address.save()
    return redirect('shopping:shoppingn')


@login_required
@require_GET
def change_active_address(request, address_id):
    pass_active_address = request.user.addresses.filter(is_active=True)[0]
    pass_active_address.is_active = False
    pass_active_address.save()

    now_active_address = get_object_or_404(Address, id=address_id, user=request.user)
    now_active_address.is_active = True
    now_active_address.save()
    return JsonResponse({"status": 'ok'})
