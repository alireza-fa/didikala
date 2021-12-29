from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .forms import UserChangeForm, UserCreationForm
from .models import User, Score
from django.contrib.auth.models import Group


class ScoreAdmin(admin.StackedInline):
    model = Score
    extra = 1


class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm
    list_display = ('username', 'email', 'is_active', 'is_admin')
    list_filter = ('is_active', 'is_admin')
    fieldsets = (
        (None, {'fields': ('username', 'email', 'password', 'fullname', 'phone_number', 'city')}),
        ('Personal info', {'fields': ('is_active', )}),
        ('Permission', {'fields': ('is_admin', )}),
    )

    add_fieldsets = (None, {"fields": ('username', 'email', 'password1', 'password2')},)
    search_fields = ('email', 'username')
    ordering = ('username',)
    filter_horizontal = ()
    inlines = (ScoreAdmin, )


admin.site.register(User, UserAdmin)
admin.site.unregister(Group)
