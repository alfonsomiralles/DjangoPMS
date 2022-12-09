from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import SetPasswordForm
from django.contrib.auth import get_user_model

class UpdateUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = '__all__'

class SetPasswordForm(SetPasswordForm):
    class Meta:
        model = get_user_model()
        fields = ['new_password1', 'new_password2']        