from django import forms
from django.contrib.auth.forms import UserCreationForm
from flimsystripsapp.models import User
from django.forms import ModelForm


class RegistrationForm(forms.ModelForm):
    email = forms.EmailField(max_length=254, required=True)
    password = forms.CharField(widget=forms.PasswordInput())
    password_confirmation = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('email',)

    def clean(self):
        cleaned_data = super(RegistrationForm, self).clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("password_confirmation")

        if password != confirm_password:
            raise forms.ValidationError(
                "Password confirmation does not match"
            )
    
    def save(self, commit=True):
        user = super(RegistrationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user
