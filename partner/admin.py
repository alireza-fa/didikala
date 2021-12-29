from django.contrib import admin
from .models import Partner, PartnerStock


@admin.register(Partner)
class PartnerAdmin(admin.ModelAdmin):
    pass


@admin.register(PartnerStock)
class PartnerStockAdmin(admin.ModelAdmin):
    pass
