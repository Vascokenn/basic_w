from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField

from phonenumber_field.formfields import PhoneNumberField
from .models import User


class AddUserForm(forms.ModelForm):
    password1 = forms.CharField(
        label='Password', widget=forms.PasswordInput
    )
    password2 = forms.CharField(
        label='Confirm password', widget=forms.PasswordInput
    )
    phone_number = PhoneNumberField(
        label="Phone Number",
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Enter Phone Number'}),
    )

    class Meta:
        model = User
        fields = ('email','phone_number', 'first_name', 'last_name', 'role')

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords do not match")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UpdateUserForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = (
            'email', 'password', 'first_name', 'role', 'last_name', 'is_active',
            'is_staff', 'phone_number'
        )

    def clean_password(self):
        return self.initial["password"]


class UserAdmin(BaseUserAdmin):
    form = UpdateUserForm
    add_form = AddUserForm

    list_display = ('email', 'phone_number','first_name', 'last_name', 'role', 'is_staff', )
    list_filter = ('is_staff',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'role', 'phone_number')}),
        ('Permissions', {'fields': ('is_active', 'is_staff')}),
    )
    add_fieldsets = (
        (
            None,
            {
                'classes': ('wide',),
                'fields': (
                    'email', 'first_name', 'last_name', 'role', 'password1',
                    'password2', 'phone_number'
                )
            }
        ),
    )
    search_fields = ('email', 'first_name', 'last_name', 'phone_number')
    ordering = ('email', 'first_name', 'last_name')
    filter_horizontal = ()


admin.site.register(User, UserAdmin)
