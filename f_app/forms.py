from django import forms
from django.contrib.auth.forms import UserChangeForm, PasswordChangeForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
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
	
	def __init__(self, *args, **kwargs):
		self.user = kwargs.pop('user', None)
		super(UrlForm, self).__init__(*args, **kwargs)
		self.fields['name'].widget.attrs.update({'class': 'edIn1', 'placeholder': 'URL Name'})
		self.fields['url'].widget.attrs.update({'class': 'edIn1', 'placeholder': 'https://'})
		self.fields['checking_length'].widget.attrs.update({'class': 'edIn1'})
		self.fields['updating_time'].widget.attrs.update({'class': 'edIn1'})
	

	def clean_name(self):
		name = self.cleaned_data.get('name')
		name = name.lower()
		return name
	
	def clean(self):
		data = super().clean()
		name = data.get('name')
		url = data.get('url')
		if UrlModel.objects.filter(user=self.user, name=name, url=url).exists():
			raise ValidationError("You already have a URL with this Name and Link")
		return data
	