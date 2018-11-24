from django import forms
from .models import User


class AuthForm(forms.Form):
    login = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput)


class SignUpFrom(forms.Form):
    login = forms.CharField(max_length=100)
    email = forms.EmailField(max_length=100)
    nickname = forms.CharField(max_length=100, required=False)
    password = forms.CharField(widget=forms.PasswordInput)
    password_confirmation = forms.CharField(widget=forms.PasswordInput)
    photo = forms.ImageField(initial='uploads/default_image.jpg', required=False)

    def clean(self):
        if self.cleaned_data['password'] != self.cleaned_data['password_confirmation']:
            raise self.add_error('password_confirmation', 'Пароли не совпадают')

        return self.cleaned_data

    def clean_login(self):
        login = self.cleaned_data['login']
        if User.objects.filter(username=login).exists():
            raise forms.ValidationError('Пользователь с таким логином уже существует')

        return login

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Пользователь с таким email уже существует')

        return email

    def save(self):
        user = User.objects.create_user(login=self.cleaned_data['login'], email=self.cleaned_data['email'],
                                        nickname=self.cleaned_data['nickname'], password=self.cleaned_data['password'],
                                        photo=self.cleaned_data['photo'])
        user.save()
        return user
