from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core import validators
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.db.models import Q
from accounts.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import PasswordResetForm, SetPasswordForm

error_msg = {
    "required": 'این فیلد اجباری است',
    "invalid": 'ایمیل وارد شده معتبر نمیباشد',
}


class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'email')

    def clean_password2(self):
        cd = self.cleaned_data
        if not cd['password1'] and cd['password2'] and cd['password1'] != cd['password2']:
            raise forms.ValidationError('passwords must be match')
        return cd['password2']

    def save(self, commit=True):
        cd = self.cleaned_data
        user = super().save(commit=False)
        user.set_password(cd['password1'])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ('username', 'email', 'phone_number', 'password')

    def clean_password(self):
        return self.initial['password']


class UserLoginForm(forms.Form):
    remember_me = forms.BooleanField(
        widget=forms.CheckboxInput({"class": 'custom-control-input'}),
        required=False,
        error_messages=error_msg,
    )
    username = forms.CharField(
        widget=forms.TextInput(attrs={"class": 'input-ui pr-2', "placeholder": 'ایمیل یا نام کاربری خود را وارد نمایید'}),
        required=True,
        error_messages=error_msg,
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": 'input-ui pr-2', "placeholder": 'رمز عبور خود را وارد نمایید'}),
        required=True,
        error_messages=error_msg,
    )

    def login(self, request):
        cd = self.cleaned_data
        user = authenticate(request, username=cd['username'], password=cd['password'])
        if user is not None:
            login(request, user)
            if not cd['remember_me']:
                request.session.set_expiry(0)
            return True
        return False


class UserRegistrationForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={"class": 'input-ui pr-2', "placeholder": 'ایمیل یا نام کاربری خود را وارد نمایید'},
        ),
        required=True,
        error_messages=error_msg,
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"class": 'input-ui pr-2', "placeholder": 'رمز عبور خود را وارد نمایید'}
        ),
        required=True,
        error_messages=error_msg,
    )
    conditions = forms.BooleanField(
        widget=forms.CheckboxInput(
            attrs={"class": 'custom-control-input', "id": 'customCheck3'}
        ),
        required=False,
    )

    def check_email(self):
        username = self.cleaned_data['username']
        try:
            validate_email(username)
            return True
        except ValidationError:
            return False

    def clean_username(self):
        user = User.objects.filter(Q(username=self.cleaned_data['username']) | Q(email=self.cleaned_data['username']))
        if user.exists():
            raise forms.ValidationError('اطلاعات وارد شده قبلا ثبت شده است')
        return self.cleaned_data['username']

    def clean_password(self):
        if len(self.cleaned_data['password']) < 8:
            raise forms.ValidationError('رمز عبور نمیتواند از هشت کاراکتر کمتر باشد')
        return self.cleaned_data['password']

    def clean_conditions(self):
        if not self.cleaned_data['conditions']:
            raise forms.ValidationError('لطفا حریم خصوصی و شرایط را بخوانید و تایید کنید')
        return self.cleaned_data['conditions']

    def save(self, request):
        cd = self.cleaned_data
        check_mail = self.check_email()
        if check_mail:
            user = User(email=cd['username'])
            user.set_password(cd['password'])
            user.save()
            use_log = authenticate(request, username=self.cleaned_data['username'], password=self.cleaned_data['password'])
            if use_log:
                login(request, use_log)
                return user
        user = User(username=cd['username'])
        user.set_password(cd['password'])
        user.save()
        use_log = authenticate(request, username=self.cleaned_data['username'], password=self.cleaned_data['password'])
        if use_log:
            login(request, use_log)
            return user


class UserChangePasswordForm(forms.Form):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": 'input-ui pr-2', "placeholder": 'رمز عبور خود را وارد نمایید'}),
        required=True,
        error_messages=error_msg,
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": 'input-ui pr-2', "placeholder": 'رمز عبور خود را وارد نمایید'}),
        required=True,
        error_messages=error_msg,
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": 'input-ui pr-2', "placeholder": 'رمز عبور خود را وارد نمایید'}),
        required=True,
        error_messages=error_msg,
    )

    def __init__(self, user=None, *args, **kwargs):
        super(UserChangePasswordForm, self).__init__(*args, **kwargs)
        self.user = user

    def clean_password(self):
        if not self.user.check_password(self.cleaned_data['password']):
            raise forms.ValidationError('پسورد وارد شده صحیح نمیباشد')
        return self.cleaned_data['password']

    def check_pass(self):
        cd = self.cleaned_data
        if cd['password1'] != cd['password2']:
            return False
        return True

    def save(self, request, password):
        user = User.objects.get(id=request.user.id)
        if user:
            user.set_password(password)
            user.save()
            return user
        return None


class ProfileAdditionalForm(forms.Form):
    first_name = forms.CharField(
        widget=forms.TextInput(attrs={"class": 'input-ui pr-2', "placeholder": 'نام خود را وارد نمایید'}),
        required=False,
    )
    fullname = forms.CharField(
        widget=forms.TextInput(attrs={"class": 'input-ui pr-2', "placeholder": 'نام خانوادگی خود را وارد نمایید'}),
        required=False,
    )
    code_melli = forms.CharField(
        widget=forms.TextInput(attrs={"class": 'input-ui pl-2 text-left dir-ltr', "placeholder": '-'}),
        required=False
    )
    phone_number = forms.CharField(
        widget=forms.TextInput(attrs={
            "class": 'input-ui pl-2 text-left dir-ltr', "placeholder": 'شماره موبایل خود را وارد نمایید'}
        ),
        required=False,
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            "class": 'input-ui pl-2 text-left dir-ltr', "placeholder": 'آدرس ایمیل خود را وارد نمایید'}
        ),
        required=True,
        error_messages=error_msg
    )
    image = forms.ImageField(
        widget=forms.FileInput(attrs={
            "class": 'custom-file-input', "id": 'inputGroupFile04', "aria-describedby": 'inputGroupFileAddon04'}
        ),
        required=False
    )
    card_number = forms.CharField(
        widget=forms.TextInput(attrs={"class": 'input-ui pl-2 text-left dir-ltr', "placeholder": '-'}),
        required=False,
        validators=[
            validators.MinValueValidator(16, 'شماره کارت معتبر نمیباشد'),
            validators.MaxValueValidator(16, 'شماره کارت معتبر نمیباشد')
        ]
    )
    foreign_person = forms.BooleanField(
        widget=forms.CheckboxInput(attrs={"class": 'custom-control-input', "id": 'customCheck3'}),
        required=False
    )
    shared_news = forms.BooleanField(
        widget=forms.CheckboxInput(attrs={"class": 'custom-control-input', "id": 'customCheck4'}),
        required=False
    )

    def __init__(self, user=None, *args, **kwargs):
        super(ProfileAdditionalForm, self).__init__(*args, **kwargs)
        self.user = user

    def clean_first_name(self):
        if self.cleaned_data['first_name']:
            if not 3 <= len(self.cleaned_data['first_name']) <= 32:
                raise forms.ValidationError('اسم باید بین ۳ و ۳۲ کاراکتر باشد')
        return self.cleaned_data['first_name']

    def clean_fullname(self):
        if self.cleaned_data['fullname']:
            if not 6 <= len(self.cleaned_data['fullname']) <= 64:
                raise forms.ValidationError('نام و نام خانوادگی باید بین ۶ و ۶۴ کاراکتر باشد')
        return self.cleaned_data['fullname']

    def clean_phone_number(self):
        if self.cleaned_data['phone_number']:
            if not 10 <= len(self.cleaned_data['phone_number']) <= 18:
                raise forms.ValidationError('شماره موبایل وارد شده معتبر نمیباشد')
        return self.cleaned_data['phone_number']

    def clean_card_number(self):
        if self.cleaned_data['card_number']:
            if not 16 <= len(self.cleaned_data['card_number']) <= 16:
                raise forms.ValidationError('شماره کارت وارد شده معتبر نمیباشد')
        return self.cleaned_data['card_number']

    def clean_email(self):
        use = User.objects.filter(email=self.cleaned_data['email'])
        if use.exists():
            if use[0] != self.user:
                raise forms.ValidationError('این ایمیل متعلق به شخص دیگری هست😔😔')
        return self.cleaned_data['email']

    def save(self, user):
        cd = self.cleaned_data
        if cd['first_name']:
            user.first_name = cd['first_name']
        if cd['fullname']:
            user.fullname = cd['fullname']
        if cd['code_melli']:
            user.code_melli = cd['code_melli']
        if cd['phone_number']:
            user.phone_number = cd['phone_number']
        if cd['email']:
            user.email = cd['email']
        if cd['card_number']:
            user.card_number = cd['card_number']
        if cd['foreign_person']:
            user.foreign_person = cd['foreign_person']
        if cd['shared_news']:
            user.received_news = cd['shared_news']
        return user


class UserPasswordResetForm(PasswordResetForm):
    def __init__(self, *args, **kwargs):
        super(UserPasswordResetForm, self).__init__(*args, **kwargs)

    email = forms.EmailField(widget=forms.EmailInput(
        attrs={"class": 'input-ui pr-2', "placeholder": 'ایمیل خود را وارد نمایید'}),
        error_messages=error_msg
    )


class UserPasswordResetConfirmForm(SetPasswordForm):
    def __init__(self, *args, **kwargs):
        super(UserPasswordResetConfirmForm, self).__init__(*args, **kwargs)

    new_password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': "input-ui pr-2", "placeholder": 'رمز عبور جدید را وارد نمایید'}),
        error_messages=error_msg
    )
    new_password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": "input-ui pr-2", "placeholder": 'تکرار رمز عبور خود را وارد نمایید'}),
        error_messages=error_msg
    )
