from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import gettext_lazy as _

# Get user model currently in use
User = get_user_model()


class UserLoginForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(
        attrs={'class': 'form-control mb-3', 'placeholder': 'Email', 'id': 'login-username'}))
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class':'form-control'}), required=True, label='Password',
    )
    remember_me = forms.BooleanField(
        widget=forms.CheckboxInput, required=False, label='Remember me'
    )

    # class Meta:
    #     model = User
    #     fields = ('email',)
    #     required = ('email',)
    #     labels = {
    #         'email': _('Email Address'),
    #     }
    #     widgets = {
    #         'email': forms.EmailInput(attrs={'class':'form-control'}),
    #     }



class UserRegistrationForm(UserCreationForm):
    password1 = forms.CharField(label='Enter Password', widget=forms.PasswordInput, required=True)
    password2 = forms.CharField(
        label='Confirmation Password', widget=forms.PasswordInput, required=True,
        help_text='Passwords are case-sensitive.',
    )

    class Meta:
        model = User
        fields = ('email', 'username',)
        required = ('email', 'username',)
        labels = {
            'email': _('Email Address'),
        }
        help_texts = {
            'email': _('An email will be sent to the address for verification.'),
            'username': _('Username may contain letters, numbers and symbols.'),
        }


class UserUpdateForm(forms.ModelForm):

    email = forms.EmailField(
        label='Account email (can not be changed)', max_length=200, widget=forms.EmailInput(
            attrs={'class': 'form-control mb-3', 'placeholder': 'email', 'id': 'form-email', 'readonly': 'readonly'}))

    name = forms.CharField(
        label='Full Name', min_length=4, max_length=50, widget=forms.TextInput(
            attrs={'class': 'form-control mb-3', 'placeholder': 'eg john doe', 'id': 'form-name'}))

    username = forms.CharField(
        label='username', min_length=4, max_length=50, widget=forms.TextInput(
            attrs={'class': 'form-control mb-3', 'placeholder': 'eg. Pablo', 'id': 'form-username'}))

    class Meta:
        model = User
        fields = ('email', 'name', 'username',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].required = True
        self.fields['email'].required = True
