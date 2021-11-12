from django import forms
from django.contrib.auth import get_user_model

from .models import Order


User = get_user_model()




class OrderForm(forms.ModelForm):

    order_date = forms.DateField(widget=forms.TextInput(attrs={'type': 'date'}))
    address = forms.CharField(required=True)
    class Meta:
        model = Order
        fields = (
            'first_name', 'last_name', 'phone', 'buying_type', 'address', 'order_date', 'comment'
        )


    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)
        self.fields['order_date'].label = 'Дата получения заказа'
        self.fields['address'].label = 'Адрес'
        self.fields['phone'].widget.attrs['class'] = "number"
        self.fields['first_name'].widget.attrs['class'] = "char"
        self.fields['last_name'].widget.attrs['class'] = "char"

    def clean_phone(self):
        phone = self.cleaned_data['phone']
        if not(10 < len(phone) < 14):
            print('err')
            raise forms.ValidationError('Неверно указан номер телефона.')
        return phone

    def clean(self):

        return self.cleaned_data



class LoginForm(forms.ModelForm):

    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:

        model = User
        fields = ('email', 'password')


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].widget.attrs['placeholder'] = 'Почта'
        self.fields['password'].widget.attrs['placeholder'] = 'Пароль'


    def clean_email(self):

        email = self.cleaned_data['email']
        if not User.objects.filter(email=email).exists():
            raise forms.ValidationError(f'Пользователь с логином {email} не найден.')
        return email

    def clean_password(self):

        email = self.data.get('email')
        password = self.cleaned_data['password']
        user = User.objects.filter(email=email).first()

        if user:
            if not user.check_password(password):
                raise forms.ValidationError('Неверный пароль.')

        return password


    def clean(self):

        return self.cleaned_data



class RegistrationForm(forms.ModelForm):

    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)
    # phone = forms.CharField(required=True)
    # address = forms.CharField(required=True)
    # email = forms.CharField(required=True)

    class Meta:
        model = User
        fields = ('email', 'password', 'confirm_password')

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)
        self.fields['email'].widget.attrs['placeholder'] = 'Почта'
        self.fields['password'].widget.attrs['placeholder'] = 'Пароль'
        self.fields['confirm_password'].widget.attrs['placeholder'] = 'Подтвердите пароль'
        # self.fields['phone'].widget.attrs['placeholder'] = 'Номер телефона'
        # self.fields['first_name'].widget.attrs['placeholder'] = 'Имя'
        # self.fields['last_name'].widget.attrs['placeholder'] = 'Фамилия'
        # self.fields['address'].widget.attrs['placeholder'] = 'Адрес'
        # self.fields['email'].widget.attrs['placeholder'] = 'Электронная почта'


    def clean_email(self):

        try:
            email = self.cleaned_data['email']
            email_name, email_address = email.split('@')
            email_address, email_domain = email_address.split('.')

        except ValueError:
            raise forms.ValidationError('Некорректный email-адрес.')

        if len(email_name) < 1 or len(email_address) < 1 or len(email_domain) < 1:
            raise forms.ValidationError('Некорректный email-адрес.')

        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Аккаунт с таким email-адресом уже зарегистрирован.')

        return email


    def clean_password(self):

        password = self.cleaned_data['password']
        confirm_password = self.data.get('confirm_password')

        if password != confirm_password:
            raise forms.ValidationError('Пароли не совпадают.')

        return password


    def clean(self):

        return self.cleaned_data