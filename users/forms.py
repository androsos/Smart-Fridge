from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile

class UserRegisterForm(UserCreationForm):
	email = forms.EmailField()

	class Meta:
		model = User #peirazoume to user model
		fields = ['username', 'email', 'password1', 'password2'] #poia fields exoume sto form

class UserUpdateForm(forms.ModelForm):
	email = forms.EmailField()

	class Meta:
		model = User #peirazoume to user model
		fields = ['username', 'email'] #poia fields exoume sto form
		
class ProfileUpdateForm(forms.ModelForm):
	class Meta:
		model = Profile
		fields = ['image']
		