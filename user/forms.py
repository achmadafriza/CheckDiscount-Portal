from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate
from django.utils.translation import gettext, gettext_lazy as _

from .models import Profile

class RegistrationForm(UserCreationForm):
    email = forms.EmailField()
    first_name = forms.CharField()
    last_name = forms.CharField()
    phone_number = forms.CharField()

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'phone_number', 'username', 'password1', 'password2']

# https://stackoverflow.com/questions/46459258/how-to-inform-a-user-that-he-is-not-active-in-django-login-view
class LoginForm(AuthenticationForm):
    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username is not None and password:
            self.user_cache = authenticate(self.request, username=username, password=password)
            if self.user_cache is None:
                try:
                    user_temp = User.objects.get(username=username)
                except:
                    user_temp = None

                if user_temp is not None and user_temp.check_password(password):
                        self.confirm_login_allowed(user_temp)
                else:
                    raise forms.ValidationError(
                        self.error_messages['invalid_login'],
                        code='invalid_login',
                        params={'username': self.username_field.verbose_name},
                    )

        return self.cleaned_data
    
    def confirm_login_allowed(self, user):
        if not user.is_active:
            raise forms.ValidationError(
            _("Your account has expired/not verified. Please verify by clicking the link below"),
            code='inactive',
        )

class OTPForm(forms.Form):
    otp_number = forms.CharField(min_length=64, max_length=64)

class StaffPermissionForm(forms.Form):
    permission = forms.ChoiceField(
        choices=[
            ('is_admin', 'Admin'),
            ('is_staff', 'Staff')
        ],
        widget=forms.RadioSelect
    )