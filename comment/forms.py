from django import forms
from django.core import validators

from .models import Comment

error_msg = {
    "required": 'این فیلد اجباری است'
}


class CommentAddForm(forms.Form):
    subject = forms.CharField(
        max_length=120,
        widget=forms.TextInput(attrs={"class": 'input-ui pr-2', "placeholder": 'عنوان نظر خود را بنویسید'}),
        error_messages=error_msg,
        required=True
    )
    positive_point = forms.CharField(
        max_length=500,
        widget=forms.TextInput(
            attrs={"class": 'input-ui pr-2 ui-input-field', "id": 'advantage-input', "autocomplete": 'off'}),
        required=False,
    )
    negative_point = forms.CharField(
        max_length=500,
        widget=forms.TextInput(
            attrs={"class": 'input-ui pr-2 ui-input-field', "id": 'advantage-input', "autocomplete": 'off'}),
        required=False,
    )
    body = forms.CharField(
        widget=forms.Textarea(attrs={"class": 'input-ui pr-2 pt-2', "rows": 5, "placeholder": 'متن خود را بنویسید'}),
        error_messages=error_msg,
        required=True
    )
    CHOICES = (
        (1, 'پیشنهاد میکنم'),
        (2, 'خیر،پیشنهاد نمی کنم'),
        (3, 'نظری ندارم'),
    )
    suggest = forms.ChoiceField(
        choices=CHOICES,
        widget=forms.RadioSelect(),
        required=False
    )
    quality = forms.CharField(
        widget=forms.TextInput(
            attrs={"id": 'ex19', "type": 'text', "data-provide": 'slider', "data-slider-ticks": '[1, 2, 3, 4, 5]',
                   "data-slider-ticks-labels": '["خیلی بد", "بد", "معمولی","خوب","عالی"]',
                   "data-slider-min": '1', "data-slider-max": '5', "data-slider-step": '1',
                   "data-slider-value": '3', "data-slider-tooltip": 'hide'})
    )
    cost = forms.CharField(
        widget=forms.TextInput(
            attrs={"id": 'ex19', "type": 'text', "data-provide": 'slider', "data-slider-ticks": '[1, 2, 3, 4, 5]',
                   "data-slider-ticks-labels": '["خیلی بد", "بد", "معمولی","خوب","عالی"]',
                   "data-slider-min": '1', "data-slider-max": '5', "data-slider-step": '1',
                   "data-slider-value": '3', "data-slider-tooltip": 'hide'})
    )
    innovation = forms.CharField(
        widget=forms.TextInput(
            attrs={"id": 'ex19', "type": 'text', "data-provide": 'slider', "data-slider-ticks": '[1, 2, 3, 4, 5]',
                   "data-slider-ticks-labels": '["خیلی بد", "بد", "معمولی","خوب","عالی"]',
                   "data-slider-min": '1', "data-slider-max": '5', "data-slider-step": '1',
                   "data-slider-value": '3', "data-slider-tooltip": 'hide'})
    )
    features = forms.CharField(
        widget=forms.TextInput(
            attrs={"id": 'ex19', "type": 'text', "data-provide": 'slider', "data-slider-ticks": '[1, 2, 3, 4, 5]',
                   "data-slider-ticks-labels": '["خیلی بد", "بد", "معمولی","خوب","عالی"]',
                   "data-slider-min": '1', "data-slider-max": '5', "data-slider-step": '1',
                   "data-slider-value": '3', "data-slider-tooltip": 'hide'})
    )
    easiness = forms.CharField(
        widget=forms.TextInput(
            attrs={"id": 'ex19', "type": 'text', "data-provide": 'slider', "data-slider-ticks": '[1, 2, 3, 4, 5]',
                   "data-slider-ticks-labels": '["خیلی بد", "بد", "معمولی","خوب","عالی"]',
                   "data-slider-min": '1', "data-slider-max": '5', "data-slider-step": '1',
                   "data-slider-value": '3', "data-slider-tooltip": 'hide'})
    )
    designing = forms.CharField(
        widget=forms.TextInput(
            attrs={"id": 'ex19', "type": 'text', "data-provide": 'slider', "data-slider-ticks": '[1, 2, 3, 4, 5]',
                   "data-slider-ticks-labels": '["خیلی بد", "بد", "معمولی","خوب","عالی"]',
                   "data-slider-min": '1', "data-slider-max": '5', "data-slider-step": '1',
                   "data-slider-value": '3', "data-slider-tooltip": 'hide'})
    )

    def save(self, user, product):
        cd = self.cleaned_data
        comment = Comment(
            user=user, product=product, subject=cd['subject'], body=cd['body'], quality=cd['quality'], cost=cd['cost'],
            innovation=cd['innovation'], features=cd['features'], easiness=cd['easiness'], designing=cd['designing']
        )
        if cd['positive_point']:
            comment.positive_point = cd['positive_point']
        if cd['negative_point']:
            comment.negative_point = cd['negative_point']
        if cd['suggest']:
            comment.suggest = cd['suggest']
        comment.save()
        return comment


class QuestionForm(forms.Form):
    name = forms.CharField(
        max_length=64,
        widget=forms.TextInput(attrs={"class": 'form-control col-md-3', "placeholder": 'نام شما'}),
        required=True
    )
    body = forms.CharField(
        widget=forms.Textarea(attrs={"class": 'form-control mb-3', "rows": '5', "placeholder": 'متن پرسش شما'}),
        required=True
    )
    notify = forms.BooleanField(
        widget=forms.CheckboxInput(attrs={"class": 'custom-control-input', "id": 'customCheck3'}),
        required=False
    )

    def clean_name(self):
        if len(self.cleaned_data['name']) > 64:
            raise forms.ValidationError('نام نمیتواند بیش از ۶۴ کاراکتر باشد')
        return self.cleaned_data['name']
