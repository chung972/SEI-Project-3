from django import forms
from django.db.models.fields import BigIntegerField
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import Profile


class LoginForm(forms.Form):
    username = forms.CharField(label="Username", max_length=64)
    password = forms.CharField(label="Password", widget=forms.PasswordInput())


class ExtendedUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2')
    email = forms.EmailField(max_length=30)
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)

    def save(self, commit=True):
        user = super().save(commit=False)

        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']

        if commit:
            user.save()
        return user


class ExtendedUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name')

    def save(self, commit=True):
        user = super().save(commit=False)

        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']

        if commit:
            user.save()
        return user


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('phone_number', 'affiliations')
    # apparently, for regular forms (i.e. not ModelForms), you have to use
    # 'required' as an option and not 'blank'
    affiliations = forms.CharField(max_length=100, required=False)
    # TODO: figure out how the FUCK to make phone_number, or more specifically,
    # IntegerField() to be null
    
    phone_number = BigIntegerField(null=True, blank=True)

    def save(self, commit=True):
        profile = super().save(commit=False)

        profile.affiliations = self.cleaned_data['affiliations']
        profile.phone_number = self.cleaned_data['phone_number']

        if commit:
            profile.save()
        return profile

