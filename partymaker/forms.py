from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django import forms

from partymaker.models import User, Order


class AuthForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['name', 'photo']

    def __init__(self, *args, **kwargs):
        super(AuthForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_action = 'auth'
        self.helper.add_input(Submit('submit', 'Авторизоваться'))


class OrderForm(forms.ModelForm):
    is_member = forms.ChoiceField(required=True, choices=Order.MEMBER_CHOICE, label='Вы прийдете?')
    drink = forms.ChoiceField(required=True, choices=Order.DRINK_CHOICE, label='Что будете пить?')

    class Meta:
        model = Order
        fields = ['is_member', 'drink']

    def __init__(self, *args, **kwargs):
        super(OrderForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_action = 'order'
        self.helper.add_input(Submit('submit', 'Отправить'))
