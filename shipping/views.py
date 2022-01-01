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
@require_http_methods(request_method_list=['GET', 'POST'])
def edit_address(request, address_id):
    address = get_object_or_404(Address, id=address_id, user=request.user)
    if request.method == 'POST':
        form = EditAddressForm(request.POST)
        if form.is_valid():
            form.edit(user=request.user, address=address)
        return redirect('accounts:profile_address')
    else:
        form = EditAddressForm(initial={
            "fullname": address.fullname, "phone_number": address.phone_number,
            "postal_address": address.postal_address, "postal_code": address.postal_code,
            "province": address.province, "city": address.city
        })
    return render(request, 'shipping/edit_address.html', {"form": form})


@login_required
@require_GET
def delete_address(request, address_id):
    address = get_object_or_404(Address, id=address_id, user=request.user)
    address.delete()
    return redirect('accounts:profile_address')


def active_address(request, address_id):
    ac_address = get_object_or_404(Address, is_active=True, user=request.user)
    ac_address.is_active = False
    ac_address.save()
    address = get_object_or_404(Address, id=address_id, user=request.user, is_active=False)
    address.is_active = True
    address.save()
    return redirect('shopping:shoppingn')
