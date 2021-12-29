from django import template
from django.shortcuts import get_object_or_404

from shipping.forms import AddAddressForm, EditAddressForm
from shipping.models import Address

register = template.Library()


@register.simple_tag
def add_address():
    return AddAddressForm()


@register.simple_tag
def edit_address():
    return EditAddressForm()
