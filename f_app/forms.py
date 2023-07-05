from django import forms
from django.contrib.auth.forms import UserChangeForm, PasswordChangeForm
from django.contrib.auth.models import User

from f_app.models import UrlModel


class EditUserForm(UserChangeForm):
	class Meta:
		model = User
		fields = ['username', 'email', 'first_name', 'last_name']

class ChangePasswordForm(PasswordChangeForm):
	new_password1 = forms.CharField(max_length=50, widget=forms.PasswordInput, required=True)
	class Meta:
		fields = ['__all__']

class UrlForm(forms.ModelForm):
	class Meta:
		model  = UrlModel
		fields = ['name', 'url', 'checking_length', 'updating_time']