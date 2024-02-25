from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm
from phonenumber_field.formfields import PhoneNumberField
from account.models import User

class EmployeeRegistrationForm(UserCreationForm):
    phone_number = PhoneNumberField(
        required=False,
        label="Phone Number",
        widget=forms.TextInput(attrs={'placeholder': 'Enter Phone Number'}),
    )
    
    def __init__(self, *args, **kwargs):
        UserCreationForm.__init__(self, *args, **kwargs)
        #self.fields['gender'].required = False
        #self.fields.pop('gender')  # Remove the gender field

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'phone_number', 'password1', 'password2']

    def save(self, commit=True):
        user = UserCreationForm.save(self, commit=False)
        user.role = "employee"
        if commit:
            user.save()
        return user

class EmployerRegistrationForm(UserCreationForm):
    phone_number = PhoneNumberField(
        required=False,
        label="Phone Number",
        widget=forms.TextInput(attrs={'placeholder': 'Enter Phone Number'}),
    )

    def __init__(self, *args, **kwargs):
        UserCreationForm.__init__(self, *args, **kwargs)
        self.fields.pop('gender')  # Remove the gender field

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'phone_number', 'password1', 'password2']

    def save(self, commit=True):
        user = UserCreationForm.save(self, commit=False)
        user.role = "employer"
        if commit:
            user.save()
        return user

class UserLoginForm(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'placeholder': 'Email'})
    )
    password = forms.CharField(strip=False, widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))
    # ... (other code remains unchanged)

class EmployeeProfileEditForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(EmployeeProfileEditForm, self).__init__(*args, **kwargs)
        self.fields.pop('gender')  # Remove the gender field
    class Meta:
        model = User
        fields = ["first_name", "last_name"]
