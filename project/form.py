from django import forms
from django.contrib.auth.models import User
from project.models import UserProfile, Message

class UserForm(forms.ModelForm):

    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = {"username", "password", "email"}

class UserProfileForm(forms.ModelForm):

    class Meta:
        model = UserProfile
        fields = {"profile_name", "profile_last_name", "profile_department", "profile_age", "profile_pic"}

class Send_message(forms.ModelForm):
    class Meta:
        model = Message
        fields = {"content"}