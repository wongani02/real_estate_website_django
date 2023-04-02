from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import gettext_lazy as _

from .models import Profile

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


class UserRegistrationForm(forms.ModelForm):
    CHOICES = (
        ('Customer', 'Customer'),
        ('Realtor', 'Realtor'),
    )
    name = forms.CharField(label='Fullname', min_length=4, max_length=50, help_text='Required')
    username = forms.CharField(label='Username', min_length=4, max_length=50, help_text='Required')
    email = forms.EmailField(label='Email', max_length=100, help_text='Required', error_messages={'required': 'this field is required'})
    user_type = forms.ChoiceField(
        choices=CHOICES,
        widget=forms.Select(attrs={'class' :'form-control w-100'})
    )
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Re-enter Password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('name', 'email','username','user_type',)

    # def clean_user_name(self):
    #     user_name = self.cleaned_data['name'].lower()
    #     r = Customer.objects.filter(user_name=user_name)
    #     if r.count():
    #         raise forms.ValidationError("Username already exists")
    #     return user_name

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Passwords do not match.')
        return cd['password2']

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError(
                'Please use another Email, that is already taken')
        return email

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update(
            {'class': 'form-control mb-3', 'placeholder': 'Full name'})
        self.fields['username'].widget.attrs.update(
            {'class': 'form-control mb-3', 'placeholder': 'username'})
        self.fields['email'].widget.attrs.update(
            {'class': 'form-control mb-3', 'placeholder': 'E-mail', 'name': 'email', 'id': 'id_email'})
        self.fields['password'].widget.attrs.update(
            {'class': 'form-control mb-3', 'placeholder': 'Password'})
        self.fields['password2'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Repeat Password'})


class UserUpdateForm(forms.ModelForm):

    email = forms.EmailField(
        label='Account email (can not be changed)', max_length=200, widget=forms.EmailInput(
            attrs={'class': 'form-control form_control', 'placeholder': 'email', 'id': 'form-email', 'readonly': 'readonly'}))

    name = forms.CharField(
        label='Full Name', min_length=4, max_length=50, widget=forms.TextInput(
            attrs={'class': 'form-control form_control', 'placeholder': 'Full Name', 'id': 'form-name'}))

    username = forms.CharField(
        label='username', min_length=4, max_length=50, widget=forms.TextInput(
            attrs={'class': 'form-control form_control', 'placeholder': 'eg. Pablo', 'id': 'form-username'}))

    class Meta:
        model = User
        fields = ('email', 'name', 'username',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].required = True
        self.fields['email'].required = True


class UserProfileForm(forms.ModelForm):
    other_email = forms.EmailField(
        label='other email', max_length=200, widget=forms.EmailInput(
            attrs={'class': 'form-control form_control', 'placeholder': 'other email', 'id': 'form-other_email'}),
            required=False)
    
    phone_number = forms.CharField(
        label='Phone', min_length=4, max_length=10, widget=forms.TextInput(
            attrs={'class': 'form-control form_control', 'placeholder': 'Phone number', 'id': 'form-phone_number'}),
            required=False)

    phone_number_2 = forms.CharField(
        label='Phone', min_length=4, max_length=10, widget=forms.TextInput(
            attrs={'class': 'form-control form_control', 'placeholder': 'Phone (other)', 'id': 'form-phone_number_2'}),
            required=False)
    
    bio = forms.CharField(
        label='Bio', min_length=10,  widget=forms.Textarea(
            attrs={'class': 'form-control form_control', 'rows':6, 'placeholder': 'Bio.....', 'id': 'form-bio'}),
            required=False)
    
    profile_img = forms.ImageField(
        label='Bio', widget=forms.FileInput(
            attrs={'class': 'form-control form_control','name':'image1', 'id': 'image1', 'accept':'.gif, .jpg, .png'}),
            required=False)
    
    class Meta:
        model = Profile
        fields = ('other_email', 'phone_number', 'phone_number_2', 'bio', 'profile_img',)

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.fields['name'].required = True
    #     self.fields['email'].required = True
