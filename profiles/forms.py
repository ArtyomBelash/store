from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import Profile


class ProfileRegister(UserCreationForm):
    email = forms.EmailField(label='Email')

    class Meta:
        model = Profile
        fields = ('username', 'email', 'password1', 'password2', 'picture')
        labels = {'username': 'Логин',
                  'picture': 'Фото'}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['placeholder'] = 'Имя пользователя'
        self.fields['email'].widget.attrs['placeholder'] = 'Email'
        self.fields['password1'].widget.attrs['placeholder'] = 'Пароль'
        self.fields['password2'].widget.attrs['placeholder'] = 'Повторите пароль'
