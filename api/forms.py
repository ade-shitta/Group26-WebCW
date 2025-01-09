from django import forms
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Row, Layout, Submit
from crispy_forms.bootstrap import FormActions
from .models import User, Hobby

class LoginForm(forms.Form):
    '''Form for user login'''
    username = forms.CharField(
        label='Username',
        max_length=50,
        widget=forms.TextInput(attrs={'autocomplete': 'username'})
    )
    password = forms.CharField(
        label='Password',
        max_length=50,
        widget=forms.PasswordInput(attrs={'autocomplete': 'password'})
    )

    helper = FormHelper()
    helper.form_id = 'login-form'
    helper.layout = Layout(
        Row('username', css_class="mb-2"),
        Row('password', css_class="mb-2"),
        FormActions(
            Submit('login', 'Log in', css_class="btn-primary mt-2"),
        )
    )

class SignUpForm(UserCreationForm):
    '''Form for user registration'''
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'autocomplete': 'email'})
    )
    date_of_birth = forms.DateField(
        required=True,
        widget=forms.DateInput(attrs={'type': 'date'})
    )
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)

    helper = FormHelper()
    helper.form_id = 'signup-form'
    helper.layout = Layout(
        Row('username', css_class='mb-2'),
        Row('email', css_class='mb-2'),
        Row('first_name', 'last_name', css_class='mb-2'),
        Row('date_of_birth', css_class='mb-2'),
        Row('password1', css_class='mb-2'),
        Row('password2', css_class='mb-2'),
        FormActions(
            Submit('signup', 'Sign up', css_class="btn-primary mt-3"),
        )
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', 
                 'first_name', 'last_name', 'date_of_birth')

class UserUpdateForm(forms.ModelForm):
    '''Form for updating user profile'''
    email = forms.EmailField(required=True)
    date_of_birth = forms.DateField(
        required=True,
        widget=forms.DateInput(attrs={'type': 'date'})
    )
    hobbies = forms.ModelMultipleChoiceField(
        queryset=Hobby.objects.all(),
        required=False,
        widget=forms.SelectMultiple(attrs={'class': 'form-select'})
    )

    helper = FormHelper()
    helper.form_id = 'profile-update-form'
    helper.layout = Layout(
        Row('username', css_class='mb-2'),
        Row('email', css_class='mb-2'),
        Row('first_name', 'last_name', css_class='mb-2'),
        Row('date_of_birth', css_class='mb-2'),
        Row('hobbies', css_class='mb-2'),
        FormActions(
            Submit('update', 'Update Profile', css_class="btn-primary mt-3"),
        )
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 
                 'date_of_birth', 'hobbies')

class HobbyForm(forms.ModelForm):
    '''Form for creating new hobbies'''
    name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    helper = FormHelper()
    helper.form_id = 'hobby-form'
    helper.layout = Layout(
        Row('name', css_class='mb-2'),
        FormActions(
            Submit('create', 'Add Hobby', css_class="btn-primary mt-2"),
        )
    )

    class Meta:
        model = Hobby
        fields = ('name',)

class PasswordChangeCustomForm(PasswordChangeForm):
    '''Custom form for changing password'''
    helper = FormHelper()
    helper.form_id = 'password-change-form'
    helper.layout = Layout(
        Row('old_password', css_class='mb-2'),
        Row('new_password1', css_class='mb-2'),
        Row('new_password2', css_class='mb-2'),
        FormActions(
            Submit('change', 'Change Password', css_class="btn-primary mt-3"),
        )
    )
