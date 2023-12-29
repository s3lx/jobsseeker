from django import forms
from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.hashers import check_password

from scraping.models import Language

User = get_user_model()

class UserLoginForm(forms.Form):

    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    def clean(self, *args, **kwargs):

        email = self.cleaned_data.get('email').strip()
        password = self.cleaned_data.get('password').strip()

        if email and password:
            qs = User.objects.filter(email=email)
            if not qs.exists():
                raise forms.ValidationError("There is no such user")
            if not check_password(password, qs[0].password):
                raise forms.ValidationError("Incorrect password")
            user = authenticate(email=email, password=password)
            if not user:
                raise forms.ValidationError("This account is deactivated")
        return super(UserLoginForm, self).clean(*args, **kwargs)



class UserRegistrationForm(forms.ModelForm):
    email = forms.EmailField(label='Enter you email',widget=forms.EmailInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label='Password',widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label='Retype password for confirmation',widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ('email',)

    def clean_password2(self):
        data = self.cleaned_data
        if data['password'] != data['password2']:
            raise forms.ValidationError("Passwords doesn't match")
        return data['password2']


class UserUpdateForm(forms.Form):
    language = forms.ModelChoiceField(queryset=Language.objects.all(),
                                      to_field_name="slug",
                                      required=True, widget=forms.Select(attrs={'class': 'form-control'}),
                                      label='Speciality')

    send_email = forms.BooleanField(required=False, widget=forms.CheckboxInput,
                                    label='Would you like to receive a newsletter?')

    class Meta:
        model = User
        fields = ('language','send_email')


class ContactForm(forms.Form):
    language = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'form-control'}),
                                      label='Speciality')

    email = forms.EmailField(label='Enter email',required=True,
                             widget=forms.EmailInput(attrs={'class': 'form-control'}))
