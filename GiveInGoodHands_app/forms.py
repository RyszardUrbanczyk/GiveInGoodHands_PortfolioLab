from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from GiveInGoodHands_app.models import Donation, Category


class AddDonationForm(forms.ModelForm):
    categories = forms.ModelMultipleChoiceField(queryset=Category.objects.all(),
                                                widget=forms.CheckboxSelectMultiple)

    class Meta:
        model = Donation
        fields = '__all__'


class RegisterForm(forms.Form):
    name = forms.CharField(widget=forms.TextInput(attrs={'autocomplete': 'off', 'placeholder': 'Imię'}))
    surname = forms.CharField(widget=forms.TextInput(attrs={"autocomplete": "off", 'placeholder': 'Nazwisko'}))
    email = forms.CharField(widget=forms.EmailInput(attrs={"autocomplete": "off", 'placeholder': 'E-mail'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Hasło'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Powtórz hasło'}))

    # def clean(self):
    #     cleaned_data = super().clean()
    # if cleaned_data['password1'] != cleaned_data['password2']:
    #     raise ValidationError("Wpisłeś różne hasła!")
    # if User.objects.filter(username=cleaned_data['email']).exists():
    #     raise ValidationError('Istnieje taki adres e-mail w bazie!')


class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.EmailInput(attrs={'placeholder': 'użytkownik'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'hasło'}))
